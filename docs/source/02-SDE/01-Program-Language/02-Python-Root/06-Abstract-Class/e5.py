# -*- coding: utf-8 -*-

"""

"""

import abc


class PersonAbc(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def say_hello_to(self, name: str):
        raise NotImplementedError


class Person(PersonAbc):
    def say_hello_to(self, name: str):
        print(f"Hello {name}, my name is {self.name}")


def validate(person: Person):
    person.say_hello_to(name="Mr X")


person = Person(name="Alice")
validate(person)
person.say_hello_to(name="Bob")
