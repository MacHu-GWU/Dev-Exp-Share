# -*- coding: utf-8 -*-

from s3pathlib import S3Path, context
from pathlib_mate import Path
from boto_session_manager import BotoSesManager

dir_home = Path.home()
dir_repo_list = [
    Path(dir_home, "Documents", "CodeCommit", "aws_data_lab_open_source_infra-project")
]
s3path_prefix = S3Path.from_s3_uri("s3://663351365541-us-east-1-artifacts/aws-data-lab-sanhe-code-commit")

bsm = BotoSesManager(profile_name="sanhe_admin_for_opensource")
context.attach_boto_session(boto_ses=bsm.boto_ses)

for dir_repo in dir_repo_list:
    path_repo_zip = dir_repo.change(new_basename=dir_repo.basename + ".zip")
    dir_repo.make_zip_archive(dst=path_repo_zip, overwrite=True)
    s3path = S3Path(s3path_prefix, path_repo_zip.basename)
    s3path.upload_file(path=path_repo_zip.abspath, overwrite=True)
