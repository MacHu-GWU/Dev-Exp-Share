# -*- coding: utf-8 -*-

from rich import print as rprint
from pathlib import Path
from boto_session_manager import BotoSesManager

# we have two accounts, one for dev and one for prod
bsm_dev = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
bsm_prod = BotoSesManager(profile_name="bmt_app_prod_us_east_1")

# the layer is published on dev account
layer_name = "aws_lambda_layer_test"
layer_version = 1
layer_arn = f"arn:aws:lambda:us-east-1:{bsm_dev.aws_account_id}:layer:{layer_name}:{layer_version}"
print(layer_arn)


def get_layer_from_dev_account():
    res = bsm_dev.lambda_client.get_layer_version_by_arn(Arn=layer_arn)
    rprint(res)


def get_layer_from_prod_account():
    res = bsm_prod.lambda_client.get_layer_version_by_arn(Arn=layer_arn)
    rprint(res)


def grant_permission():
    # use the target (grantee) account ID for principal
    res = bsm_dev.lambda_client.add_layer_version_permission(
        LayerName=layer_name,
        # you cannot use wild card in version number
        VersionNumber=layer_version,
        # the statement ID is the unique identifier for this permission
        # I suggest this naming convention  "account-${aws_account_id}"
        StatementId=f"account-{bsm_prod.aws_account_id}",
        # if you use "*", then it is public available
        Principal=bsm_prod.aws_account_id,
        Action="lambda:GetLayerVersion",
    )
    rprint(res)


def revoke_permission():
    res = bsm_dev.lambda_client.remove_layer_version_permission(
        LayerName=layer_name,
        VersionNumber=layer_version,
        # the statement ID has to match the one you used to grant permission
        StatementId=f"account-{bsm_prod.aws_account_id}",
    )
    rprint(res)


def deploy_lambda_function_using_shared_layer_on_target_account():
    """
    If you want to deploy a lambda function from dev to prod and the layer is
    on dev account. You just need to use an IAM Role on dev as your main role,
    then assume the prod role. That prod role has the permission to deploy
    lambda function ot it's own account, that's it. There's no need to explicitly
    give the prod role permission to get the layer version on dev account, you
    already did that using account id as the principal.
    """
    # deploy from dev to prod account
    # dev role assume the prod role
    bsm_assume_prod = bsm_dev.assume_role(
        role_arn=f"arn:aws:iam::{bsm_prod.aws_account_id}:role/cross-account-deployer-role"
    )
    zipfile = Path(__file__).absolute().parent.joinpath("source.zip").read_bytes()
    res = bsm_assume_prod.lambda_client.create_function(
        FunctionName="layer-sharing-test",
        Runtime="python3.8",
        Handler="lambda_function.lambda_handler",
        Code={
            "ZipFile": zipfile,
        },
        Role=f"arn:aws:iam::{bsm_assume_prod.aws_account_id}:role/lambda-poweruser-role",
        Timeout=3,
        MemorySize=128,
        Layers=[layer_arn],
    )
    rprint(res)

# get_layer_from_dev_account()
# get_layer_from_prod_account()
# grant_permission()
# revoke_permission()
# deploy_lambda_function_using_shared_layer_on_target_account()