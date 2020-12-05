# -*- coding: utf-8 -*-

import attr
import enum


@attr.s
class Status:
    id = attr.ib()
    name = attr.ib()
    description = attr.ib()


class Mixin:
    def say_hi(self):
        print(f"Hi, my name is {self.name}, how are you?")



@attr.s
class Person(Mixin):
    name = attr.ib()


@attr.s
class Student(Person):
    student_id = attr.ib()


@attr.s
class Teacher(Person):
    teacher_id = attr.ib()


teacher = Teacher(name="Alice", teacher_id="Good")
print(teacher)
teacher.say_hi()