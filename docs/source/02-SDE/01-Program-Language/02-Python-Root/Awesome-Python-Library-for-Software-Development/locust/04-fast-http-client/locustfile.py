 # -*- coding: utf-8 -*-

"""
假设我们的 API 是一个接受 ``{"name": "Alice"}`` 返回 ``"Hello Alice"`` 的一个 POST
接口.

Locust 默认使用 requests 发起 HTTP 请求. 但 Locust 基于 gevent 有一个内置的异步协程
FastHTTPUser, 可以在单机提供更高的并发.
"""

import json
from locust import FastHttpUser, task, constant

headers = {
    "Authorization": "allow",
    "Content-Type": "application/json",
}

class MyUser(FastHttpUser):
    # 所有的 HTTP request 可以用相对路径, endpoint domain 则放在 host 变量里
    host = "https://your-api-endpoint/"

    # 每个 User 在 run 一个 Task 以后会等待一段时间再 Run 下一个
    # 如果 wait time = 0.1 秒, 而设置 100 个 User, 那么每秒则会发起 10 个请求
    # 一般我们会将其设置为 1, 这样 User 总数就等于并发总数
    # 这个数还可以是一个随机值, 你只需要 from locust import between, 然后用 between(1, 3)
    # 就可以指定 1 ~ 3 秒随机延迟
    wait_time = constant(1)

    @task
    def index(self):
        response = self.client.post(
            "/hello",
            headers=headers,
            data=json.dumps({"name": "Alice"})
        )
        print(response.text)
