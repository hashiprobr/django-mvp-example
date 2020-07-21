from example.consumers import UploadConsumer

from .consumers import ChatConsumer


routesuffixes = {
    r'upload': UploadConsumer,
    r'chat': ChatConsumer,
}
