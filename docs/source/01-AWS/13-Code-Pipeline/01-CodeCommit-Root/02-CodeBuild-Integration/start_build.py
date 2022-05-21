# -*- coding: utf-8 -*-

from rich import print as rprint
from boto_session_manager import BotoSesManager, AwsServiceEnum

bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_2")
cb_client = bsm.get_client(AwsServiceEnum.CodeBuild)

res = cb_client.start_build(
    projectName="learn_codebuild_single",
    # sourceVersion="refs/heads/master",
    # sourceVersion="refs/heads/feature",
    # sourceVersion="86c5afba16f586592ec30efaebbc9c3a868a05c8",
)
rprint(res)
