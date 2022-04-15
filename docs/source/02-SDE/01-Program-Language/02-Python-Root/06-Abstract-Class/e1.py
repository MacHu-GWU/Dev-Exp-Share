# -*- coding: utf-8 -*-

import abc
import pytest


class Animal(abc.ABC):
    @abc.abstractmethod
    def bark(self):
        raise NotImplementedError


with pytest.raises(TypeError):
    animal = Animal()


class Dog(Animal):
    def bark(self):
        print("wong wong!")


dog = Dog()
