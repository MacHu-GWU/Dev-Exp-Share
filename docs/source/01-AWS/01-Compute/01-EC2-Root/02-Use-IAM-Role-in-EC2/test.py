# -*- coding: utf-8 -*-

import boto3
from troposphere_mate import (
    Template,
    Ref,
    ec2, iam,
    upload_template, deploy_stack,
)
from troposphere_mate.canned.iam import (
    AWSServiceName, AWSManagedPolicyArn, create_assume_role_policy_document
)

aws_profile = "eq_sanhe"
image_id = "ami-00dc79254d0461090"  # amazon linux
security_group_id = "sg-2c2b857d"  # allow ssh
key_name = "eq-sanhe-dev"
stack_name = "eq-sanhe-test"

template = Template()

iam_role_allow_ec2_access_s3 = iam.Role(
    "IamRoleEc2AccessS3",
    template=template,
    RoleName="ec2-s3-read-only",
    AssumeRolePolicyDocument=create_assume_role_policy_document([
        AWSServiceName.amazon_Elastic_Compute_Cloud_Amazon_EC2
    ]),
    ManagedPolicyArns=[
        AWSManagedPolicyArn.amazonS3ReadOnlyAccess,
    ],
)

iam_instance_profile_allow_ec2_access_s3 = iam.InstanceProfile(
    "IamInstanceProfile",
    template=template,
    InstanceProfileName="ec2-inst-profile-s3-read-only",
    Roles=[
        Ref(iam_role_allow_ec2_access_s3)
    ],
)

ec2_inst = ec2.Instance(
    "Ec2Instance",
    template=template,
    ImageId=image_id,
    InstanceType="t2.micro",
    SubnetId="subnet-1d8dbc41",
    SecurityGroupIds=[
        security_group_id,
    ],
    KeyName=key_name,
    IamInstanceProfile=Ref(iam_instance_profile_allow_ec2_access_s3),
)

boto_ses = boto3.Session(profile_name=aws_profile)
s3_client = boto_ses.client("s3")
cf_client = boto_ses.client("cloudformation")

template_url = upload_template(
    s3_client=s3_client,
    template_content=template.to_json(),
    bucket_name="eq-sanhe-for-everything"
)
deploy_stack(
    cf_client=cf_client,
    stack_name=stack_name,
    template_url=template_url,
    include_iam=True,
)
