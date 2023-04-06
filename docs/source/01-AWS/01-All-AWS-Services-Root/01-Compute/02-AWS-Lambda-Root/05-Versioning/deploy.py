# -*- coding: utf-8 -*-

import cottonformation as ctf
from cottonformation.res import iam, awslambda

# create a ``Template`` object to represent your cloudformation template
tpl = ctf.Template(
    Description="Aws Lambda Versioning Example",
)

iam_role_for_lambda = iam.Role(
    "IamRoleForLambdaExecution",
    rp_AssumeRolePolicyDocument=ctf.helpers.iam.AssumeRolePolicyBuilder(
        ctf.helpers.iam.ServicePrincipal.awslambda()
    ).build(),
    p_RoleName="lbd-versioning-poc",
    p_ManagedPolicyArns=[
        ctf.helpers.iam.AwsManagedPolicy.AmazonDynamoDBFullAccess,
    ]
)
tpl.add(iam_role_for_lambda)


lbd_func = awslambda.Function(
    "LbdFuncVersioningPOC",
    rp_Code=awslambda.PropFunctionCode(
        p_S3Bucket="sanhe-admin-for-everything",
        p_S3Key="lambda/MacHu-GWU/lbd-versioning/066212d310fb9d829154d197be860d0f.zip",
    ),
    rp_Role=iam_role_for_lambda.rv_Arn,
    p_FunctionName="lbd-versioning-poc",
    p_MemorySize=256,
    p_Timeout=3,
    p_Runtime=ctf.helpers.awslambda.LambdaRuntime.python36,
    p_Handler="lbd_handler.main",
    ra_DependsOn=iam_role_for_lambda,
    p_Tags=ctf.Tag.make_many(Stage="Dev", Description="Changed"),
)
tpl.add(lbd_func)

if __name__ == "__main__":
    import boto3

    boto_ses = boto3.session.Session(profile_name="sanhe")
    env = ctf.Env(boto_ses=boto_ses)
    env.deploy(
        template=tpl,
        stack_name="lbd-versioning-poc",
        bucket_name="sanhe-admin-for-everything",
        include_iam=True,
    )