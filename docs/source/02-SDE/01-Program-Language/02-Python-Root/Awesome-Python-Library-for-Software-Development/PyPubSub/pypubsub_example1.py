# -*- coding: utf-8 -*-

"""
对于 Publisher Subscriber 这种观察者模式的实现有很多种. 生产环境中比较常用的是类似于
Kafka, AWS SNS, 这种通过网络进行通信的服务.

而 PyPubSub 则是一个 in memory 的实现. publisher 和 subscriber 的通信是在内存内部
通信的, 不经过任何网络以及端口.
"""

from pubsub import pub


# ------------ create a listener ------------------
def listener1(message):
    print("User1 received Message: {}".format(message))


def listener2(message):
    print("User2 received Message: {}".format(message))


# ------------ register listener ------------------
pub.subscribe(listener=listener1, topicName="NewsFeed")
pub.subscribe(listener=listener2, topicName="NewsFeed")


# ---------------- send a message ------------------
pub.sendMessage(topicName="NewsFeed", message="Hello World")
