# -*- coding: utf-8 -*-

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
