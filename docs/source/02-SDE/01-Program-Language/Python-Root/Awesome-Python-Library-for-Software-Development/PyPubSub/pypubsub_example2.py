# -*- coding: utf-8 -*-

"""
在下面的例子中我们可以很清楚的看到, pubsub 他并不是异步地将 message 广播出去, 而是按照顺序
执行. 也就是说如果有 N 个 subscriber, 只有第一个 subscriber 消费完才能轮到第二个 subscriber
"""

import time
from pubsub import pub


# ------------ create a listener ------------------
def listener1(message):
    for ith in range(1, 1+10):
        time.sleep(1)
        print("{}: User1 received Message: {}".format(ith, message))


def listener2(message):
    for ith in range(1, 1+10):
        time.sleep(1)
        print("{}: User2 received Message: {}".format(ith, message))


# ------------ register listener ------------------
pub.subscribe(listener=listener1, topicName="NewsFeed")
pub.subscribe(listener=listener2, topicName="NewsFeed")


# ---------------- send a message ------------------
pub.sendMessage(topicName="NewsFeed", message="Hello World")
