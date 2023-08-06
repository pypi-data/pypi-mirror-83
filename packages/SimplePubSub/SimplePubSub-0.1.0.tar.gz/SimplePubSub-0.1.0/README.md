# How to use:

The Publisher
-------------

Simply:
```
# import Publisher
from gabriel import Publisher

# instantiate a publisher object
publisher = Publisher()

# send a message
# default topic is "default"
publisher.send("hello")
```

With a topic:
```
# import Publisher
from gabriel import Publisher

# instantiate a publisher object
publisher = Publisher()

# send a message
publisher.send("hello", topic="greetings")
```

With a custom Redis backend:
```
# import Publisher
from gabriel import Publisher

# instantiate a publisher object using the backend_url
# from https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Endpoints.html
publisher = Publisher(backend_url="redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379")
```

Infinitely publish:
```
from gabriel import Publisher

publisher = Publisher()

while True:
    # get some data from somewhere
    message, topic = custom_get_message_and_topic()
    # publish it
    publisher.send(message, topic)
```


The Subscriber
--------------

Simply:
```
# import Subscriber
from gabriel import Subscriber

# instantiate a publisher object
subscriber = Subscriber()
subscriber.subscribe("greetings")

# receive a message if there is one
# could be a message or None
message = subscriber.receive()

# or wait (in a locking way) until there is one
message = subscriber.receive(wait=True)
```

With a custom Redis backend:
```
# import Subscriber
from gabriel import Subscriber

# instantiate a subscriber object
# from https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Endpoints.html
subscriber = Subscriber(backend_url="redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379")
```

Infinitely subscribe:
```
# import Subscriber
from gabriel import Subscriber

# instantiate a subscriber object
subscriber = Subscriber()
subscriber.subscribe("greetings")

# receive messages infinitely
for message in subscriber:
    transformed_message = custom_transform(message)
    ...
```

Or with a timeout, before the last message
```
# import Subscriber
from gabriel import Subscriber

# instantiate a subscriber object
# set a 60 second timer
subscriber = Subscriber(timeout=60)
subscriber.subscribe("greetings")

# receive messages until 60 seconds after the last message
try:
    for message in subscriber:
        transformed_message = custom_transform(message)
        ...
except TimeoutError:
    pass
```


Poll every 60s: (will get all messages from the queue per poll)
```
# import Subscriber
from gabriel import Subscriber

# instantiate a subscriber object
# set a 60 second refresh rate
subscriber = Subscriber(refresh_rate=60)
subscriber.subscribe("greetings")

# poll the backend every 60s and get everything in it
for message in subscriber:
    transformed_message = custom_transform(message)
    ...
```

The Message
-----------

```
>>> from gabriel import Subscriber, Message
>>> subscriber = Subscriber()
>>> subscriber.subscribe("greetings")
>>> message = subscriber.receive(wait=True)
>>> message
Message(channel=greetings, text=hello)
>>> message.channel
'greetings'
>>> message.text
'hello'
```
