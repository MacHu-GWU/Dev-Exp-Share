# -*- coding: utf-8 -*-

"""
Sample script. Invoke codebuild job, build from repo hosted in codecommit.
Can build from default source, master branch, specific branch, specific commit.
"""

from rich import print as rprint
from boto_session_manager import BotoSesManager, AwsServiceEnum

bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_2")
cb_client = bsm.get_client(AwsServiceEnum.CodeBuild)

res = cb_client.start_build(
    projectName="learn_codebuild_single",
    # no sourceVersion, use default source, usually the master

    # build from master branch, latest code
    # sourceVersion="refs/heads/master",

    # build from specific branch
    # sourceVersion="refs/heads/feature1-add-buildspec-file",

    # build from specific commit
    # sourceVersion="86c5afba16f586592ec30efaebbc9c3a868a05c8",
)
rprint(res["build"]["id"])
rprint(res["build"]["arn"])
