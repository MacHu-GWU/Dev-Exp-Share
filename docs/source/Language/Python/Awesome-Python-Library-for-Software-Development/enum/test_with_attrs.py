# -*- coding: utf-8 -*-

import enum

import attr


@attr.s
class StatusDetail:
    id = attr.ib(type=int, default=None)
    name = attr.ib(type=str, default=None)


# @enum.unique
class Status(enum.Enum):
    s1 = StatusDetail(id=1, name="name_s1")
    s2 = StatusDetail(id=2, name="name_s2")
    s3 = StatusDetail(id=3, name="name_s3")

    def __init__(self, sd: StatusDetail):
        self._value_ = sd.id
        self.obj = sd

    # @classmethod
    # def return_detail_by_id(cls, id):
    #     pass


# assert Status["s1"].value == 1
# assert Status["s1"].obj == 1

testcases = [
    Status.s1,
    Status["s1"],
    Status(1),
]


def run_test(testcase):
    assert testcase.name == "s1"
    assert testcase.value == 1
    assert testcase.obj.id == 1
    assert testcase.obj.name == "name_s1"


for testcase in testcases:
    run_test(testcase)

# print(Status(1).value, Status(1).obj)


# for status in Status:
#     print(status)
# status.value.name = status.name
# status.value.description = f"description for status {status.value.id}"

# print(Status["s1"])
class Coordinate(bytes, enum.Enum):
    """
    Coordinate with binary codes that can be indexed by the int code.
    """

    def __new__(cls, value, label, unit):
        # print(value, label, unit)
        obj = bytes.__new__(cls)
        # print(type(obj))
        obj._value_ = value
        obj.label = label
        obj.unit = unit
        return obj

    PX = (0, 'P.X', 'km')
    PY = (1, 'P.Y', 'km')
    VX = (2, 'V.X', 'km/s')
    VY = (3, 'V.Y', 'km/s')


testcases = [
    Coordinate.PX,
    Coordinate["PX"],
    Coordinate(0),
]

def run_test(testcase):
    assert testcase.name == "PX"
    assert testcase.value == 0
    assert testcase.label == "P.X"
    assert testcase.unit == "km"

# for testcase in testcases:
#     run_test(testcase)

# print(Coordinate['PY'])

# print(isinstance(Coordinate.PY, Coordinate))
# print(type(Coordinate.PY.value))

# print(Coordinate(3).label)
