from example.consumers import UploadConsumer

from .consumers import ChatConsumer


routesuffixes = {
    r'upload': UploadConsumer.as_asgi(),
    r'chat': ChatConsumer.as_asgi(),
}
