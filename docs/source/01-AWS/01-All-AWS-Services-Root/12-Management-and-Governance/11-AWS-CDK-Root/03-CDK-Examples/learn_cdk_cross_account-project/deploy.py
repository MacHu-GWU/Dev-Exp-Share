# -*- coding: utf-8 -*-

import subprocess
from pathlib_mate import Path
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
bsm_prod = bsm.assume_role(
    role_arn="arn:aws:iam::216242137773:role/cross-account-deployer-role"
)

dir_here = Path.dir_here(__file__)


def cdk_deploy():
    args = [
        "cdk",
        "deploy",
        "--all",
        "--require-approval",
        "never",
    ]
    with bsm_prod.awscli():
        with dir_here.temp_cwd():
            subprocess.run(args, check=True)


def cdk_delete():
    args = [
        "cdk",
        "destroy",
        "--all",
        "--force",
    ]
    with bsm_prod.awscli():
        with dir_here.temp_cwd():
            subprocess.run(args, check=True)


cdk_deploy()
# cdk_delete()
