# -*- coding: utf-8 -*-

import decorator


@decorator.decorator
def before_and_after(func, *args, **kwargs):
    print("before")
    result = func(*args, **kwargs)
    print("after")
    return result


class User:
    def __init__(self, name):
        self.name = name

    @before_and_after
    def say_hello(self):
        print(f"say_hello: Hello {self.name}")

    @property
    @before_and_after
    def greeting(self):
        print(f"greeting: Greating {self.name}")
        return None


user = User(name="Alice")

user.say_hello()
user.greeting
