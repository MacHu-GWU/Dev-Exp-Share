# -*- coding: utf-8 -*-

import abc

class Person(abc.ABC):
    @abc.abstractmethod
    def say_hello(self):
        print("Hello")


class Student(Person):
    def say_hello(self, name: str):
        super().say_hello()
        print(f"Hello {name}")

