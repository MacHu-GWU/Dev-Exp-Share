# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '123',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}

# user = User(**external_data)
# print(user.id)
# print(type(user.signup_ts), repr(user.signup_ts))
# print(user.friends)
# print(user.dict())



user = User()

# class Person(BaseModel):
#     name: str
#
#
# class Student(Person):
#     student_id: str
#
#
# class Teacher(Person):
#     teacher_id: str
#
#
# stu = Student(name="Alice", student_id="std_1")
# print(repr(stu))
#
