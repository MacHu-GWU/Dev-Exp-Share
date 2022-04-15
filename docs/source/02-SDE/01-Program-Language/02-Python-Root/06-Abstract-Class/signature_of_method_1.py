# -*- coding: utf-8 -*-

class Person:
    def say_hello(self):
        print("Hello")


class Student(Person):
    def say_hello(self, name: str):
        print(f"Hello {name}")

