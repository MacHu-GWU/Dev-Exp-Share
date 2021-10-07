# # -*- coding: utf-8 -*-
#
from pysecret import AWSSecret
#
aws_profile = "aws_data_lab_sanhe_assume_role_for_iam_test"
aws = AWSSecret(profile_name=aws_profile)
#
parameter_name = "param-store-test"
parameter_data = dict(profile=dict(name="bob"))
aws.deploy_parameter(name=parameter_name, parameter_data=parameter_data)
#
# # name = aws.get_parameter_value(parameter_name, "profile.name")
# # print(aws.parameter_cache)
# # print(name)

# import boto3
#
# ses = boto3.session.Session(profile_name=aws_profile)
# ses