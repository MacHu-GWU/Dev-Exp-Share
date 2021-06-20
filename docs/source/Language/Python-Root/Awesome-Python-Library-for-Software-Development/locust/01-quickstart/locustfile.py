# -*- coding: utf-8 -*-

from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    host = "https://www.python.org"
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get("/downloads/")
