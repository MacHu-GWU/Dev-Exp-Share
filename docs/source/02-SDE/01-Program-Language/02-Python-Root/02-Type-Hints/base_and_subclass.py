import typing as T


class Base:
    def method_base(self):
        pass

class A(Base):
    def method_a(self):
        pass


class B(Base):
    def method_b(self):
        pass

mapper: T.Dict[str, Base] = {
    "base": Base(),
    "a": A(),
    "b": B(),
}

obj: A = mapper["a"]
print(isinstance(obj, Base))