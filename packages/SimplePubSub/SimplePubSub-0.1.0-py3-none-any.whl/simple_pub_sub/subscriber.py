"""
    gabriel.subscriber
    ~~~~~~~~~

    This module implements the subscriber abstraction

"""
import time
import warnings
from collections.abc import Iterator
from typing import Union

from .backends import get_backend


class Subscriber(Iterator):
    """Subscriber is a iterator which will receive messages from "channels" or
    "topics" from backend like redis.

    How to use:
        subscriber = Subscriber()
        subscriber.subscribe("my_new_topic")
        for message in subscriber:
            print(message)


    :param backend_name: the name of the backend name type e.g. redis
    :type: str           this must be listed in the backends class attribute


    :param backend_url: the url of the backend resource, when None, it defaults
    :type: str          to the backend url of the base backend which is always
                        localhost

    :param refresh_rate: rate at which to ping the backend for new messages
    :type: int, float

    :param timeout: time before the subscriber times out after no new messages
    :type: int, float
    """

    def __init__(
        self,
        backend_name: str = "redis",
        backend_url: str = None,
        refresh_rate: Union[float, int] = None,
        timeout: Union[float, int] = None,
    ):
        # backend name
        self.backend_name = backend_name.lower()
        self._backend_class_name = self.backend_name.title() + "Backend"

        # get backend
        self._backend = get_backend(self._backend_class_name)
        # backend url
        self.backend_url = backend_url if backend_url else self._backend.BACKEND_URL
        # instantiated backend
        self.backend = self._backend(self.backend_url)

        # how often should the subscriber ping the backend for data
        # todo: implement redis timeout instead
        self.refresh_rate = refresh_rate
        if self.refresh_rate is None:
            warnings.warn("This will execute an infinite while loop")
        else:
            assert isinstance(
                self.refresh_rate, (int, float)
            ), "refresh_rate must be a number"

        # how long should the subscriber wait for a new message
        # else it will break
        self.timeout = timeout
        if self.timeout is None:
            warnings.warn("This will execute forever")
        else:
            assert isinstance(self.timeout, (int, float)), "timeout must be a number"

        # what "topics" or "channels" to subscribe to
        self.subscription = None

        # timeout is updated constantly here
        # time.time() + self.timeout
        self._current_timeout = None

    def _set_timeout(self):
        """Set _current_timeout to current time plus the user decided timeout"""
        if self.timeout:
            self._current_timeout = time.time() + self.timeout
            return
        else:
            return
            # raise ValueError("Timeout cannot be set when there is no timeout")

    def _check_not_timed_out(self):
        """Check if the subscriber is timed out.

        If there is no timeout, then the subscriber cannot be timed out and
        therefore returns False

        If there is a timeout, then check if we have set the timeout time on
        _current_timeout. If no _current_timeout has been set, then the
        _current_timeout is set by calling _set_timeout() and the function
        returns False

        If there there is a _current_timeout set, then check if time.time()
        is greater than the _current_timeout. If it is greater then the
        subscriber has timed out and a TimeoutError is raised. Otherwise
        the function returns False
        """
        if self.timeout:
            if self._current_timeout:
                if time.time() > self._current_timeout:
                    raise TimeoutError("Subscriber has timed out")
                else:
                    return False
            else:
                self._set_timeout()
                return False
        else:
            return False

    def _refresh(self):
        """Sleeps the subscriber for the user defined refresh_rate"""
        if self.refresh_rate:
            time.sleep(self.refresh_rate)
            return
        else:
            return

    # todo: add multiple subscriptions
    def subscribe(self, channel: str):
        """Subscribe the subscriber to a "channel" or "topic" by calling backend
        subscribe method

        FUTURE FEATURE: add multiple channels to subscribe too
        """
        self.subscription = channel
        return self.backend.subscribe(channel)

    # todo: implement psubscribe (pattern subscribe)
    def psubscribe(self, pattern: str):
        raise NotImplementedError()

    # todo: implement better pattern for receiving messages
    def _get_message(self):
        """Calls the backend to get a message if there is one"""
        return self.backend.receive()

    def get_message(self):
        """Gets a parsed message from backend if there is one"""
        return self.backend.parse_message(self._get_message())

    # def message(self):
    #     """Get the latest message and parse it into a Message object"""
    #     message = self.get_latest_message()
    #     yield self.backend.parse_message(message)

    # def _receive(self):
    #     """Calls the backend receive method"""
    #     return self.backend.receive()

    def receive(self, wait: bool = False):
        """Calls the backend receive method"""
        return self.get_latest_message() if wait else self.get_message()

    # todo: change for Redis.pubsub().listen()?
    def _get_latest_message(self):
        """Get the latest message from the backend. The subscriber pings the
        backend for a message, if it's there it will be returned. Otherwise the
        subscriber will check it hasn't timed out by calling
        _check_not_timed_out(), then it will wait for the length of the
        refresh_rate by calling _refresh()"""
        while True:
            # check for a message
            message = self.get_message()
            # if exists return it
            if message:
                yield message
            # else check we haven't timed out
            # then wait for the refresh rate
            else:
                self._check_not_timed_out()
                self._refresh()

    def get_latest_message(self):
        """Iterating through _get_latest_message iterator to wait until the
        latest message"""
        return next(self._get_latest_message())

    def __next__(self):
        """This is implemented to fulfill the requirements of its abstract base
        class: collections.Iterator.

        This method allows for the syntax:
        for message in subscriber:
            print(message)

        First the subscriber checks it hasn't timed out, then it gets the
        message from the message() generator. Then it resets the timeout and
        returns the message.
        """
        self._check_not_timed_out()
        message = self.get_latest_message()
        self._set_timeout()
        return message

    def get_n_latest_messages(self, n: int = 1_000) -> list:
        """
        Fetch all the available messages up until the time this method
        is called. If there are not available messages returns and empty
        list.

        NOTE: first time Mizar team has used walrus operator (MILESTONE 29-06-2020)

        :params n: maximum number of messages fetched
        :type n: int, default
        :returns: list with messages
        :rtype: list
        """

        return [
            message for _ in range(n) if (message := self.get_message()) is not None
        ]

    def get_all_latest_messages(self, max_retries: int = 10) -> list:
        """
        Get all the messages available in the queue.

        :param max_retries: number of attempts to get a message, defaults to 10
        :type max_retries: int, optional
        :return: list with messages
        :rtype: list
        """
        message_list = []
        num_retries = 1
        while num_retries < max_retries:
            message = self.get_message()
            if message is None:
                num_retries += 1
            else:
                message_list.append(message)
        return message_list

    def __iter__(self):
        """This is implemented to fulfill the requirements of its abstract base
        class: collections.Iterator."""
        return self
