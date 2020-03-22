# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mate import EngineCreator, ExtendedBase
from sfm import rnd
import random

engine = EngineCreator(
    host="rajje.db.elephantsql.com",
    database="dplfpjna",
    username="dplfpjna",
    password="lIP2DKh4WxW92bTUo6LwojnLgdmPby6D"
).create_postgresql_psycopg2()

Base = declarative_base()


class Department(Base, ExtendedBase):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Employee(Base, ExtendedBase):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    _settings_engine = engine


Base.metadata.create_all(engine)


ses = Employee.get_ses()

n_department = 3
department_list = [
    Department(department_id=1, name="HR"),
    Department(department_id=2, name="Finance"),
    Department(department_id=3, name="IT"),
]

n_employee = 50
employee_list = [
    Employee(employee_id=i+1, name=rnd.rand_hexstr(8), department_id=random.randint(1, n_department))
    for i in range(n_employee)
]

Department.smart_insert(ses, department_list)
Employee.smart_insert(ses, employee_list)


"""

machugwu
S7rXQuwhXMo^
"""