"""
    gabriel.publisher
    ~~~~~~~~~

    This module implements the publisher abstraction

"""
from .backends import get_backend


class Publisher:
    """Publisher is a object which will send messages to "channels" or "topics"
    in a backend like redis.

    How to use:
        publisher = Publisher()
        publisher.send("my first message", "my_new_topic")

    :param backend_name: the name of the backend name type e.g. redis
    :type: str           this must be listed in the backends class attribute

    :param backend_url: the url of the backend resource, when None, it defaults
    :type: str          to the backend url of the base backend which is always
                        localhost
    """

    def __init__(self, backend_name: str = "redis", backend_url: str = None):
        # backend name
        self.backend_name = backend_name.lower()
        self._backend_class_name = self.backend_name.title() + "Backend"

        # get backend
        self._backend = get_backend(self._backend_class_name)
        # backend url
        self.backend_url = backend_url if backend_url else self._backend.BACKEND_URL
        # instantiated backend
        self.backend = self._backend(self.backend_url)

    def send(self, message: str, channel: str = "default"):
        """The method to send messages to the publisher. This abstraction calls
        the backend's method for this.

        :param channel: the name of the channel to send to
        :type: str

        :param message: the message to send to the backend
        :type: str

        """
        return self.backend.send(message, channel)
