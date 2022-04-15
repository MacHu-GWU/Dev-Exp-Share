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

    # This won't work, decorator don't support working with built-in decorator
    # you need to comment this out to be able to run this script
    # @before_and_after
    # @property
    # def hello(self):
    #     print(f"hello: Hello {self.name}")
    #     return None


user = User(name="Alice")
user.say_hello()
# user.hello
