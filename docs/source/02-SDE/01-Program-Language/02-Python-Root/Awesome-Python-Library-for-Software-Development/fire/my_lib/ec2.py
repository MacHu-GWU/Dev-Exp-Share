# -*- coding: utf-8 -*-


class EC2:
    def list_instances(self):
        print("run ec2 list_instances")

    def describe_instance(self, id: str):
        print(f"run ec2 describe_instance --id={id}")
