# -*- coding: utf-8 -*-

"""
HOST = https://www.python.org

"""

import os
import time
import random

import gevent
from locust import User, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging

import pynamodb
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.exceptions import UpdateError

os.environ["AWS_DEFAULT_PROFILE"] = "aws_data_lab_sanhe_us_east_2"
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"

connection = Connection()


class Counter(Model):
    class Meta:
        table_name = "locust_test_counter_app"
        region = os.environ["AWS_DEFAULT_REGION"]
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    key = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(default=0)

    def plus_one(self):
        try:
            self.update(actions=[Counter.count.set(Counter.count + 1)])
        except UpdateError:
            self.count = 1
            self.save()

    @classmethod
    def delete_all(cls):
        with cls.batch_write() as batch:
            for item in cls.scan():
                batch.delete(item)

# Counter.delete_table()
Counter.create_table(wait=True)


class DynamodbClient:
    """
    XmlRpcClient is a wrapper around the standard library's ServerProxy.
    It proxies any function calls and fires the *request* event when they finish,
    so that the calls get recorded in Locust.
    """

    def __init__(self, host, request_event):
        self._request_event = request_event

    def plus_one(self, key: str):
        start_time = time.perf_counter()
        request_meta = {
            "request_type": "dynamodb",
            "name": "plus_one",
            "response_length": 0,
            "response": None,
            "context": {},
            "exception": None,
        }
        try:
            # --- core client logic goes here ---
            counter = Counter(key=key)
            counter.plus_one()
            # -----------------------------------
            request_meta["response"] = 1
        except Exception as e:
            request_meta["exception"] = e
        request_meta["response_time"] = (time.perf_counter() - start_time) * 1000
        self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust
        return request_meta["response"]


class DynamodbUser(User):
    """
    A minimal Locust user class that provides an XmlRpcClient to its subclasses
    """

    abstract = True  # dont instantiate this as an actual user when running Locust

    def __init__(self, environment):
        super().__init__(environment)
        self.client = DynamodbClient(self.host, request_event=environment.events.request)


# The real user class that will be instantiated and run by Locust
# This is the only thing that is actually specific to the service that we are testing.
class WebAppUser(DynamodbUser):
    host = "http://127.0.0.1:8877/"

    wait_time = between(0, 1)

    @task
    def plus_one(self):
        self.client.plus_one(key=f"key-{random.randint(1, 10)}")


def exam_dynamodb():
    time.sleep(1)
    total = 0
    for counter in Counter.scan():
        total += counter.count
    print(f"total count = {total}")


def run_locust():
    Counter.delete_all()
    time.sleep(1) # wait 1 seconds so all data is completely removed

    setup_logging("INFO", None)

    # setup Environment and Runner
    env = Environment(user_classes=[WebAppUser, ], stop_timeout=3)
    env.create_local_runner()

    # start a WebUI instance
    env.create_web_ui("127.0.0.1", 8089)

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test,
    env.runner.start(user_count=10, spawn_rate=10)

    # in 10 seconds stop the runner
    gevent.spawn_later(10, lambda: env.runner.quit())

    # wait for the greenlets
    env.runner.greenlet.join()

    # stop the web server for good measures
    env.web_ui.stop()


if __name__ == "__main__":
    run_locust()
    exam_dynamodb()
    pass
