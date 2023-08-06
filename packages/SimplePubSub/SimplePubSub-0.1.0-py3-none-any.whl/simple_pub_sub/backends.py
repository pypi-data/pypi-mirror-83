"""
    gabriel.backends
    ~~~~~~~~~

    This module implements the abstract base class: BaseBackend
    and all specific backend subclasses

"""
import sys
from abc import ABC
from abc import abstractmethod

from .message import Message


def get_backend(backend_name: str):
    """Helper function to get a type of backend from this module"""
    current_module = sys.modules[__name__]
    try:
        return getattr(current_module, backend_name)
    except AttributeError:
        raise ImportError(f"{backend_name} not available")


class BaseBackend(ABC):
    """This is an abstract base class that represents a backend resource
     e.g. Redis

    A backend should have a uniform resource locator, a publisher, a subscriber,
    a method to send to the backend, receive from the backend and to subscribe
    to the "channels" or "topics" in the backend.

    """

    @property
    @abstractmethod
    def BACKEND_URL(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def publisher(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def subscriber(self):
        raise NotImplementedError()

    @abstractmethod
    def send(self, message, channel):
        raise NotImplementedError()

    @abstractmethod
    def receive(self):
        raise NotImplementedError()

    @abstractmethod
    def subscribe(self, channel):
        raise NotImplementedError()


class RedisBackend(BaseBackend):
    """This is a specific backend configuration for Redis.

    With Redis, the publisher and subscriber can be gathered from the python
    redis library.

    :param backend_url: the url of the backend resource, when None, it defaults
    :type: str          to redis://localhost:6379

    """

    BACKEND_URL = "redis://localhost:6379"

    def __init__(self, backend_url: str = "redis://localhost:6379"):
        # set the uniform resource locator
        self.backend_url = backend_url if backend_url is not None else self.BACKEND_URL

        # try and import redis
        try:
            from redis import from_url
        except ImportError:
            raise ImportError("You must install redis")

        # get the redis client
        self.client = from_url(self.backend_url)

        self._publisher = self.client
        self._subscriber = self.client.pubsub()

        # check client is working
        response = self.client.ping()
        assert response, "redis incorrectly configured"

    @property
    def publisher(self):
        """The Redis publisher: for Redis this is just the client."""
        return self._publisher

    @property
    def subscriber(self):
        """The Redis subscriber: for Redis this is just the client however the
        pubsub() method is called to start the subscriber."""
        return self._subscriber

    def send(self, message: str, channel: str = "default"):
        """The method to send messages to the publisher: for Redis the publish()
        method is called on the client, with the channel and message.

        :param channel: the name of the channel to send to
        :type: str

        :param message: the message to send to the backend
        :type: str

        """
        return self.publisher.publish(channel, message)

    def receive(self):
        """The method to receive messages from the subscriber: for Redis this
        calls get_message() on the subscriber."""
        return self.subscriber.get_message()

    def subscribe(self, channel: str):
        """The method to subscribe to a "channel" or "topic": for Redis this
        calls the subscribe() method on the subscriber with a channel name

        :param channel: the name of the channel to receive from
        :type: str

        """
        return self.subscriber.subscribe(channel)

    @staticmethod
    def parse_message(message: dict):
        """Static method to parse a Redis message from the subscriber"""
        return Message.from_redis(message) if message else None
