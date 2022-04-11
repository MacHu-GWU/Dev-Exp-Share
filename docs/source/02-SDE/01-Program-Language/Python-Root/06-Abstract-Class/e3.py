# -*- coding: utf-8 -*-

import abc
import attr
from attrs_mate import AttrsClass

import pytest


@attr.define
class Animal(abc.ABC, AttrsClass):
    name: str = AttrsClass.ib_str()

    @abc.abstractmethod
    def bark(self):
        raise NotImplementedError


with pytest.raises(TypeError):
    animal = Animal(name="Alice's Dog")


@attr.define
class Dog(Animal):
    def bark(self):
        print(f"I am {self.name}")


dog = Dog(name="Alice's Dog")
dog.bark()
