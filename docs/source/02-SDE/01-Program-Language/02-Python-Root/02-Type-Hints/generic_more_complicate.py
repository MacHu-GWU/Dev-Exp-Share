# -*- coding: utf-8 -*-

import typing as T


class DataA:
    def is_data_a(self):
        pass


class DataB:
    def is_data_b(self):
        pass


A = T.TypeVar("A")
B = T.TypeVar("B")


# ------------------------------------------------------------------------------
# 这样做是可以的, 一次性定义两个 TypeVar 的具体类型
# ------------------------------------------------------------------------------
# class ModelA(
#     T.Generic[A, B]
# ):
#     def method1_lower(self) -> A:
#         raise NotImplementedError
#
#     def method1(self):
#         return self.method1_lower()
#
#     def method2_lower(self) -> B:
#         raise NotImplementedError
#
#     def method2(self):
#         return self.method2_lower()
#
#
# class ModelB(
#     ModelA[DataA, DataB]
# ):
#     def method1_lower(self):
#         return DataA()
#
#     def method2_lower(self):
#         return DataB()
#
#
# ModelB().method1().is_data_a()
# ModelB().method2().is_data_b()


# ------------------------------------------------------------------------------
# 如果你要用到多重继承, 一次只定义一个 TypeVar, 那么你要把两个方法分开, 分两次进行
# ------------------------------------------------------------------------------
# class BaseModelA(T.Generic[A]):
#     def method1_lower(self) -> A:
#         raise NotImplementedError
#
#     def method1(self):
#         return self.method1_lower()
#
#
# class BaseModelB(T.Generic[B]):
#     def method2_lower(self) -> B:
#         raise NotImplementedError
#
#     def method2(self):
#         return self.method2_lower()
#
#
# class ModelA(BaseModelA[DataA]):
#     def method1_lower(self):
#         return DataA()
#
#
# class ModelB(ModelA, BaseModelB[DataB]):
#     def method2_lower(self):
#         return DataB()
#
#
# ModelB().method1_lower().is_data_a()
# ModelB().method2_lower().is_data_b()


# ------------------------------------------------------------------------------
# 如果两个错综复杂要合并在一起
# ------------------------------------------------------------------------------

class ModelA(T.Generic[A]):
    def method1_lower(self) -> A:
        raise NotImplementedError

    def method1(self):
        return self.method1_lower()


class ModelB(T.Generic[B]):
    def method2_lower(self) -> B:
        raise NotImplementedError

    def method2(self):
        return self.method2_lower()


class ModelC(
    ModelA,
    ModelB,
    T.Generic[A, B],
):
    def method1_lower(self):
        return DataA()

    def method2_lower(self):
        return DataB()

    def method3_lower(self) -> T.Union[A, B]:
        raise NotImplementedError

    def method3(self):
        return self.method3_lower()


class ModelD(
    ModelC[DataA, DataB],
):
    def method3_lower(self):
        return DataA()


ModelD().method1().is_data_a()
ModelD().method2().is_data_b()
ModelD().method3().is_data_a()
