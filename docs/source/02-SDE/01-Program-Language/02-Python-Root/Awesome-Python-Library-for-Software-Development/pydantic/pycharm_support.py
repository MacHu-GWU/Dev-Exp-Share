# -*- coding: utf-8 -*-

"""
Pydantic
"""

from pydantic import BaseModel

class Base(BaseModel):
    id: int


class User(Base):
    name: str


class PaidUser(Base):
    account: str

# move cursor in brackt and hit CMD + P to see hint
Base()
User()
PaidUser()
