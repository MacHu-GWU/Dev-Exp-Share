# -*- coding: utf-8 -*-

import typing as T


class ObjectA:
    def is_object_a(self):
        print("it is object a")


class ObjectB:
    def is_object_b(self):
        print("it is object b")


A = T.TypeVar("A")
B = T.TypeVar("B")


class ModelA(
    T.Generic[A]
):
    def object_a_to_object_b(self, object_a: A) -> B:
        raise NotImplementedError

    def object_b_to_object_a(self, object_b: B) -> A:
        raise NotImplementedError


# class ModelB(
#     ModelA[ObjectA, B]
# ):
#     def object_a_to_object_b(self, object_a):
#         return ObjectB()
#
#
# class ModelC(
#     ModelB[ObjectA, ObjectB]
# ):
#     def object_b_to_object_a(self, object_b):
#         return ObjectA()
#
#
# c = ModelC()
# c.object_a_to_object_b(ObjectA()).is_object_b()
# c.object_b_to_object_a(ObjectB()).is_object_a()
