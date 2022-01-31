.. _pypi-PyPubSub:

PyPubSub - Publisher Subscriber Pattern (Pub Sub)
==============================================================================
A simple library implements Publisher Subscriber Pattern (Pub Sub).

Install: ``pip install PyPubSub``


Overview
------------------------------------------------------------------------------
对于 Publisher Subscriber 这种观察者模式的实现有很多种. 生产环境中比较常用的是类似于Kafka, AWS SNS, 这种通过网络进行通信的服务.

而 PyPubSub 则是一个 in memory 的实现. publisher 和 subscriber 的通信是在内存内部通信的, 不经过任何网络以及端口.

Pubsub 他并不是异步地将 message 广播出去, 而是按照顺序执行. 也就是说如果有 N 个 subscriber, 只有第一个 subscriber 消费完才能轮到第二个 subscriber

举例来说, 观察下面这段用 pubsub 实现的代码:

.. code-block:: python

    from pubsub import pub

    def listener1(message):
        print("User1 received Message: {}".format(message))

    def listener2(message):
        print("User2 received Message: {}".format(message))

    pub.subscribe(listener=listener1, topicName="NewsFeed")
    pub.subscribe(listener=listener2, topicName="NewsFeed")

    pub.sendMessage(topicName="NewsFeed", message="Hello World")

这段代码等效于, 不过考虑的更加周到, 功能更多:

.. code-block:: python

    from typing import List, Dict


    class Topic:
        def __init__(self, name: str):
            self.name: str = name
            self.subscribers: List[callable] = list()

        def add_subscriber(self, listener: callable):
            self.subscribers.append(listener)


    class Broker:
        def __init__(self):
            self.topics: Dict[str, Topic] = dict()

        def subscribe(self, listener: callable, topicName: str):
            if topicName in self.topics:
                topic = self.topics[topicName]
            else:
                topic = Topic(name=topicName)
                self.topics[topicName] = topic

            topic.add_subscriber(listener)

        def sendMessage(self, topicName, **kwargs):
            topic = self.topics[topicName]
            for listener in topic.subscribers:
                listener(**kwargs)


    # ------------------- usage -----------------------
    broker = Broker()


    # ------------ create a listener ------------------
    def listener1(message):
        print("User1 received Message: {}".format(message))


    def listener2(message):
        print("User2 received Message: {}".format(message))


    broker.subscribe(listener1, "NewsFeed")
    broker.subscribe(listener2, "NewsFeed")

    broker.sendMessage(topicName="NewsFeed", message="Hello World")
