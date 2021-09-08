# -*- coding: utf-8 -*-

"""
测试对于 Nested Model, Pydantic 是否能很好的支持.
"""

import enum

import pydantic


class User:
    def __init__(self, p_name):
        self.p_name = p_name


class Person(pydantic.BaseModel):
    name: str
    gender: str


class Student(Person):
    student_id: str


if __name__ == "__main__":
    # User(p_name="Alice")
    Student(name="alice", gender="female", student_id="s1")
    Student(student_id="s1")

