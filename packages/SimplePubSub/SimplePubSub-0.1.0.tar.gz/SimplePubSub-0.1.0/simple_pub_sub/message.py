"""
    gabriel.messages
    ~~~~~~~~~

    This module implements a message abstraction.

    TODO: work out if this is necessary
    The aim to to get a uniform object to handle accros all backends

"""


class Message:
    """A abstraction for message received from the Subscriber

    TODO: think about adding to producer?

    :param text: the text of the message
    :type: str

    :param channel: the name of the channel to send to, it defaults to "default"
    :type: str
    """

    __slots__ = "text", "channel", "is_subscription"

    def __init__(
        self, text: str, channel: str = "default", is_subscription: bool = False
    ):
        # TODO add more data types like JSON
        # set text
        self.text = str(text)

        # set channel
        self.channel = str(channel)

        self.is_subscription = is_subscription

    def __repr__(self):
        return f"Message(channel={self.channel}, text={self.text})"

    def __str__(self):
        return ": ".join([self.channel, self.text])

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.text == other.text and self.channel == other.channel
        else:
            return False

    @classmethod
    def from_redis(cls, message: dict):
        """Create an instance of Message for a Redis message out of the
        subscriber

        Redis subscriber returns:
            When the channel is notified of a subscription:
            {
                'type': 'subscribe',
                'pattern': None,
                'channel': b'hello',
                'data': 1
            }

            When a message is sent and got in the channel:
            {
                'type': 'message',
                'pattern': None,
                'channel': b'hello',
                'data': b'hello'
            }

        """
        text = message.get("data")
        text = text.decode() if isinstance(text, bytes) else str(text)

        channel = message.get("channel")
        channel = channel.decode() if isinstance(channel, bytes) else str(channel)

        is_subscription = message.get("type") == "subscribe"
        return cls(text=text, channel=channel, is_subscription=is_subscription)
