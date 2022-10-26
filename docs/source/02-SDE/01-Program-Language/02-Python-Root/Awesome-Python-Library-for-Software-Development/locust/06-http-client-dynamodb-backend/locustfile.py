# -*- coding: utf-8 -*-

"""
假设我们的 API 是一个接受 ``{"name": "Alice"}`` 返回 ``"Hello Alice"`` 的一个 POST
接口.

Locust 默认使用 requests 发起 HTTP 请求. 但 Locust 基于 gevent 有一个内置的异步协程
FastHTTPUser, 可以在单机提供更高的并发.
"""

from locust import HttpUser, task, between


class MyUser(HttpUser):
    host = "http://127.0.0.1:36737"

    wait_time = between(0, 1)

    @task
    def plus_one(self):
        res = self.client.post(
            url="/plus_one",
            data={"key": "k1"},
        )
        # print(res.status_code)
        # print(res.text)
