"""
    gabriel
    ~~~~~~~~~

    This is a library for publishing and subscribing. Using the pubsub workflow.

    Components:
        * A "message" or "messages" or "data"

        * A "topic" or "channel" or "theme" for the message

        * A publisher who "posts" or "sends" the message
          (Always from a python script)

        * A "backend" or "broker" who "transports" or "stores" or
          "carries" the message
          (Always another resource, e.g. Redis)

        * A subscriber who "receives" or "gets" the message from a py
          (Always from a python script)

    Core concept:
        * A python script instantiates a publisher who sends messages to a
          broker which stores the data.

        * Another python script instantiates a subscriber who receives messages
          from a broker.

        * Messages can have topics, and can be sent to different channels in the
          backend.
"""
from .message import Message
from .publisher import Publisher
from .subscriber import Subscriber

__all__ = ["Publisher", "Subscriber", "Message"]
