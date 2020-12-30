from django.conf import settings
from django.core.files.uploadhandler import TemporaryFileUploadHandler, MemoryFileUploadHandler, StopUpload
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


COOKIE_KEY = 'djangochannel'


class ChannelFileUploadHandler:
    def __init__(self, request=None):
        super().__init__(request)
        try:
            self.channel_name = request.COOKIES[COOKIE_KEY]
        except KeyError:
            self.channel_name = None

    def send_consumer(self, method, *args):
        if self.channel_name is not None:
            channel_layer = get_channel_layer()
            event = {
                'type': 'handler_' + method,
                'args': args,
            }
            async_to_sync(channel_layer.send)(self.channel_name, event)

    def file_complete(self, file_size):
        file = super().file_complete(file_size)
        self.send_consumer('complete')
        return file


class ChannelTemporaryFileUploadHandler(ChannelFileUploadHandler, TemporaryFileUploadHandler):
    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        super().handle_raw_input(input_data, META, content_length, boundary, encoding)
        self.total = content_length
        self.partial = 0
        self.progress = 0

    def receive_data_chunk(self, raw_data, start):
        super().receive_data_chunk(raw_data, start)
        self.partial = min(self.partial + self.chunk_size, self.total)
        if self.partial > settings.FILE_UPLOAD_MAX_TEMP_SIZE:
            raise StopUpload()
        progress = int(100 * (self.partial / self.total) + 0.5)
        if progress > self.progress:
            self.progress = progress
            self.send_consumer('report', self.progress)


class ChannelMemoryFileUploadHandler(ChannelFileUploadHandler, MemoryFileUploadHandler):
    pass
