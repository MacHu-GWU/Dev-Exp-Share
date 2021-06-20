# -*- coding: utf-8 -*-

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
import aws_cdk.core as core

from config import Params

env = core.Environment(region="us-east-1")


class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mk_01_db_sg()
        self.mk_02_db_subnet_group()

        self.mk_03_db_instance()
        self.mk_o_01_db_endpoint_and_port()

    def mk_01_db_sg(self):
        self.db_sg = ec2.CfnSecurityGroup(
            self, "SecurityGroupDB",
            group_name=f"{Params.project_name}-db-security-group",
            group_description="Security Group used for DB Instance",
            vpc_id=Params.vpc_id,
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="-1",
                    description="Allow any access in",
                    from_port=-1,
                    to_port=-1,
                    cidr_ip="0.0.0.0/0",
                )
            ],
            security_group_egress=[
                ec2.CfnSecurityGroup.EgressProperty(
                    ip_protocol="-1",
                    description="Allow any access out",
                    from_port=-1,
                    to_port=-1,
                    cidr_ip="0.0.0.0/0",
                )
            ],
        )

    def mk_02_db_subnet_group(self):
        self.db_subnet_group = rds.CfnDBSubnetGroup(
            self, "DBSubnetGroup",
            db_subnet_group_name=f"{Params.project_name}-db-subnet-group",
            db_subnet_group_description="DB Subnet Group for DB",
            subnet_ids=Params.subnet_ids,
        )

    def mk_03_db_instance(self):
        self.db_instance = rds.CfnDBInstance(
            self, "DBInstance",
            db_instance_class="db.t3.micro",
            db_instance_identifier=f"{Params.project_name}",
            engine="postgres",
            engine_version="11.9",
            multi_az=False,
            allocated_storage="100",
            db_subnet_group_name=self.db_subnet_group.db_subnet_group_name,
            vpc_security_groups=[
                self.db_sg.attr_group_id,
            ],
            master_username=Params.db_username,
            master_user_password=Params.db_password,
            publicly_accessible=True,
        )

    def mk_o_01_db_endpoint_and_port(self):
        self.db_endpoint = core.CfnOutput(
            self, "DBEndpoint",
            value=self.db_instance.attr_endpoint_address,
        )
        self.db_port = core.CfnOutput(
            self, "DBPort",
            value=self.db_instance.attr_endpoint_port,
        )

    def post_init_hook(self):
        self.delete()


app = core.App()

MyStack(app, f"{Params.project_name}", env=env)

app.synth()
