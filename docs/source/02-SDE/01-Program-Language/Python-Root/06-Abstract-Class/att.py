import attr

@attr.define
class User:
    name = attr.field()
    _prefix = attr.field(default="user")


user = User(name="Alice")
# print(attr.asdict(user))
print(user._prefix)