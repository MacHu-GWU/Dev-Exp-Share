# -*- coding: utf-8 -*-

import attr
import cottonformation as cf
from cottonformation.res import iam


@attr.s
class Stack(cf.Stack):
    project_name: str = attr.ib()

    @property
    def stack_name(self):
        return f"{self.project_name}-iam-roles"

    def mk_rg1(self):
        self.rg1 = cf.ResourceGroup("RG1")

        assume_role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            # Computer
                            "ec2.amazonaws.com",
                            "lambda.amazonaws.com",
                            "elasticbeanstalk.amazonaws.com",
                            "ecs.amazonaws.com",
                            "eks.amazonaws.com",
                            "glue.amazonaws.com",
                            "elasticmapreduce.amazonaws.com",
                            "cloud9.amazonaws.com",
                            # ML
                            "sagemaker.amazonaws.com",
                            "comprehend.amazonaws.com",
                            "textract.amazonaws.com",
                            # CI / CD
                            "codebuild.amazonaws.com",
                            "codedeploy.amazonaws.com",
                            # database
                            "rds.amazonaws.com",
                            "elasticache.amazonaws.com",
                            "redshift.amazonaws.com",
                            "opensearchservice.amazonaws.com",
                            # middle ware
                            "sns.amazonaws.com",
                            "sqs.amazonaws.com",
                            "kinesis.amazonaws.com",
                            # data store
                            "s3.amazonaws.com",
                        ]
                    },
                    "Action": "sts:AssumeRole"
                },
            ]
        }

        # IAM Role for all AWS Service to use with Admin access
        self.iam_role_admin = iam.Role(
            "IamRoleAdmin",
            p_RoleName=f"{self.project_name}-for-everything-admin",
            rp_AssumeRolePolicyDocument=assume_role_policy_document,
            p_ManagedPolicyArns=[
                cf.helpers.iam.AwsManagedPolicy.AdministratorAccess,
            ]
        )
        self.rg1.add(self.iam_role_admin)

    def post_hook(self):
        self.mk_rg1()


if __name__ == "__main__":
    import boto3

    stack = Stack(
        project_name="sanhe",
    )
    tpl = cf.Template(
        Description="convenient IAM Role for development",
    )
    tpl.add(stack.rg1)
    tpl.batch_tagging(ProjectName="sanhe", Creator="sanhehu@amazon.com", Longliving="True")

    boto_ses = boto3.session.Session(profile_name="aws_data_lab_sanhe", region_name="us-east-1")
    env = cf.Env(boto_ses=boto_ses)
    env.deploy(
        template=tpl,
        stack_name=stack.stack_name,
        bucket_name="aws-data-lab-sanhe-for-everything",
        include_iam=True,
    )
