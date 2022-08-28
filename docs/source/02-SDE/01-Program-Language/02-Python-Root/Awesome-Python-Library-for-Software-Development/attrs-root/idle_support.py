# -*- coding: utf-8 -*-

"""

"""

import attr

@attr.s
class Person:
    name: str
    gender: str

    def a_person_method(self):
        pass


@attr.s
class Student(Person):
    student_id: str



Student(name="a")

