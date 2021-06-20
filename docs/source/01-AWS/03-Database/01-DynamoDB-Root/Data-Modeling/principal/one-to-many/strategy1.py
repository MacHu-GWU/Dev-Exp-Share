# -*- coding: utf-8 -*-

"""
Department to Employee is One to Many.

当 Many 的那边可以 fit dynamodb 单个 record 大小时. 可以在 插入时候使用 transaction,
而在读取时, 直接从冗余中读取 many 的那部分.
"""

import os
import typing

import pynamodb
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.transactions import TransactWrite

os.environ["AWS_DEFAULT_PROFILE"] = "eq_sanhe"

connection = Connection()


class EmployeeInfoMap(MapAttribute):
    employee_id = UnicodeAttribute()
    employee_name = UnicodeAttribute()


class DepartmentModel(Model):
    class Meta:
        table_name = "one-to-many-department-1"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    department_id = UnicodeAttribute(hash_key=True)
    department_name = UnicodeAttribute()
    employees = ListAttribute(of=EmployeeInfoMap, default=lambda: [])

    @classmethod
    def _create_one(cls, department_id, department_name):
        try:
            cls.get(hash_key=department_id)
        except Model.DoesNotExist:
            cls(
                department_id=department_id,
                department_name=department_name,
                employees=[],
            ).save()

    @classmethod
    def _find_employees(cls, department_id: str) -> typing.List['EmployeeModel']:
        employee_info_map: EmployeeInfoMap
        return [
            EmployeeModel(
                employee_id=employee_info_map.employee_id,
                employee_name=employee_info_map.employee_name,
            )
            for employee_info_map in cls.get(hash_key=department_id).employees
        ]


class EmployeeModel(Model):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = "one-to-many-employee-1"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    employee_id = UnicodeAttribute(hash_key=True)
    employee_name = UnicodeAttribute()
    department_id = UnicodeAttribute(null=True)

    @classmethod
    def _create_one(cls, employee_id, employee_name, department_id=None):
        try:
            cls.get(hash_key=employee_id)
        except Model.DoesNotExist:
            if department_id is None:
                cls(
                    employee_id=employee_id,
                    employee_name=employee_name,
                    department_id=None,
                ).save()
            else:
                with TransactWrite(connection=connection) as trans:
                    trans.save(
                        cls(
                            employee_id=employee_id,
                            employee_name=employee_name,
                            department_id=department_id,
                        ),
                    )

                    trans.update(
                        DepartmentModel(department_id=department_id),
                        actions=[
                            DepartmentModel.employees.set(
                                DepartmentModel.employees.append([
                                    EmployeeInfoMap(employee_id=employee_id, employee_name=employee_name),
                                ])
                            ),
                        ]
                    )

    @classmethod
    def _assign_department(cls, employee_id, department_id: str):
        employee: EmployeeModel = cls.get(hash_key=employee_id)
        if employee.department_id == department_id:
            raise ValueError
        else:
            with TransactWrite(connection=connection) as trans:
                trans.update(
                    employee,
                    actions=[
                        EmployeeModel.department_id.set(department_id),
                    ]
                )

                trans.update(
                    DepartmentModel(department_id=department_id),
                    actions=[
                        DepartmentModel.employees.set(
                            DepartmentModel.employees.append([
                                EmployeeInfoMap(employee_id=employee_id, employee_name=employee.employee_name),
                            ])
                        ),
                    ]
                )

    @classmethod
    def _find_department(cls, employee_id: str) -> DepartmentModel:
        return DepartmentModel.get(hash_key=cls.get(hash_key=employee_id).department_id)


DepartmentModel.create_table(wait=True)
EmployeeModel.create_table(wait=True)


# --- Create Employee

def create_department():
    DepartmentModel._create_one(department_id="IT", department_name="Internet Technology")
    DepartmentModel._create_one(department_id="HR", department_name="Human Resource")


# create_department()


def create_employee():
    EmployeeModel._create_one(employee_id="e-1", employee_name="Alice", department_id="IT")
    EmployeeModel._create_one(employee_id="e-2", employee_name="Bob")
    EmployeeModel._assign_department(employee_id="e-2", department_id="HR")


# create_employee()


def find_employees():
    print([
        employee.serialize()
        for employee in DepartmentModel._find_employees(department_id="IT")
    ])


# find_employees()


def delete_all_tables():
    DepartmentModel.delete_table()
    EmployeeModel.delete_table()

# delete_all_tables()
