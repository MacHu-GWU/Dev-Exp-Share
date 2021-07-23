# -*- coding: utf-8 -*-

"""
Department to Employee is One to Many.

解决方案:

有的时候 One to Many 对应的 Many 可能数量太多, 无法作为冗余跟 One 一起储存.
这时可以以 One.id 建立 Global Index.

问题:

由于 GSI 本质是另一个 DynamoDB Table, 只不过系统帮你自动维护了. 同样的 GSI 也会根据
hash key 做 partition 分散流量. 如果 One 这边的 entity 的数量不够多. 那么会导致 GSI
的流量不均衡.
"""

import os
import random
import string
import typing

import pynamodb
from pynamodb.attributes import UnicodeAttribute
from pynamodb.connection import Connection
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.models import Model

os.environ["AWS_DEFAULT_PROFILE"] = "eq_sanhe"

connection = Connection()


class DepartmentModel(Model):
    class Meta:
        table_name = "one-to-many-department-2"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    department_id = UnicodeAttribute(hash_key=True)
    department_name = UnicodeAttribute()

    @classmethod
    def _create_one(cls, department_id, department_name):
        try:
            cls.get(hash_key=department_id)
        except Model.DoesNotExist:
            cls(
                department_id=department_id,
                department_name=department_name,
            ).save()

    # @classmethod
    # def _find_employees(cls, department_id: str):
    # employee_info_map: EmployeeInfoMap
    # return [
    #     EmployeeModel(
    #         employee_id=employee_info_map.employee_id,
    #         employee_name=employee_info_map.employee_name,
    #     )
    #     for employee_info_map in cls.get(hash_key=department_id).employees
    # ]


class DepartmentEmployeeIndex(GlobalSecondaryIndex):
    class Meta:
        index = "one-to-many-department-employee-index-2"
        projection = KeysOnlyProjection

    department_id = UnicodeAttribute(hash_key=True, null=True)


class EmployeeModel(Model):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = "one-to-many-employee-2"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    employee_id = UnicodeAttribute(hash_key=True)
    employee_name = UnicodeAttribute()
    department_id = UnicodeAttribute(null=True)
    department_index = DepartmentEmployeeIndex()

    @classmethod
    def _create_one(cls, employee_id, employee_name, department_id=None):
        try:
            cls.get(hash_key=employee_id)
        except Model.DoesNotExist:
            cls(
                employee_id=employee_id,
                employee_name=employee_name,
                department_id=department_id,
            ).save()

    @classmethod
    def _assign_department(cls, employee_id, department_id: str):
        employee: EmployeeModel = cls.get(hash_key=employee_id)
        if employee.department_id == department_id:
            raise ValueError
        else:
            employee.update(
                actions=[
                    EmployeeModel.department_id.set(department_id)
                ]
            )

    @classmethod
    def _find_department(cls, employee_id: str) -> DepartmentModel:
        return DepartmentModel.get(hash_key=cls.get(hash_key=employee_id).department_id)


DepartmentModel.create_table(wait=True)
EmployeeModel.create_table(wait=True)


class BusinessQuery:
    @classmethod
    def find_employees_by_department(cls, department_id) -> typing.Iterable[EmployeeModel]:
        return EmployeeModel.department_index.query(department_id)


# --- Create Employee

def create_department():
    DepartmentModel._create_one(department_id="IT", department_name="Internet Technology")
    DepartmentModel._create_one(department_id="HR", department_name="Human Resource")


# create_department()


def create_employee():
    def random_name():
        return "".join(random.sample(string.ascii_lowercase, 8))

    department_list = ["IT", "HR"]

    n_employee = 1000
    with EmployeeModel.batch_write() as batch:
        for i in range(1, 1 + n_employee):
            employee = EmployeeModel(
                employee_id=f"e-{i}",
                employee_name=random_name(),
                department_id=random.choice(department_list)
            )
            batch.save(employee)


# create_employee()


def find_employees():
    counter = 0
    for employee in BusinessQuery.find_employees_by_department(department_id="IT"):
        counter += 1
        print(employee.employee_id, employee.employee_name)
    print(f"total = {counter}")


find_employees()


def delete_all_tables():
    DepartmentModel.delete_table()
    EmployeeModel.delete_table()

# delete_all_tables()
