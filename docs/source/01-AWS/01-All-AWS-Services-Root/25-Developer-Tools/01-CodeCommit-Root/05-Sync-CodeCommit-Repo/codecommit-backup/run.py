# -*- coding: utf-8 -*-

import subprocess
from datetime import datetime, timezone

from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context

# ------------------------------------------------------------------------------
# update this code build to customize the behavior
# where you want to store your backup?
backup_bucket = "${backup_buccket}"
backup_folder = "projects/codecommit-backup/${codecommit_account_id}"

# list of repos you want to back up.
repo_list = [
    "${your repo name here, just repo name, not the arn}",
]

# you keep at least last N backup for each repo
keep_at_least = 3

# automatically delete backup older than N days, only if there are more than "keep_at_least" backups
retention_period = 30  # days
# ------------------------------------------------------------------------------


def backup_one_repo(repo_name):
    # clone repo
    repo_arn = f"arn:aws:codecommit:{bsm.aws_region}:{bsm.aws_account_id}:{repo_name}"
    print(f"clone repo {repo_arn}")
    args = [
        "git",
        "clone",
        "-q",
        f"codecommit::{bsm.aws_region}://{repo_name}",
        f"{repo_name}",
    ]
    subprocess.run(args, capture_output=True, check=True)

    # zip repo
    args = ["zip", "-yr", f"{repo_name}.zip", f"./{repo_name}"]
    subprocess.run(args, check=True)

    # upload repo
    time_str = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    s3_uri = f"s3://{backup_bucket}/{backup_folder}/{bsm.aws_region}/{repo_name}/{repo_name}-{time_str}.zip"
    s3path = S3Path.from_s3_uri(s3_uri)
    s3path.upload_file(f"{repo_name}.zip", overwrite=False)

    tags = {
        "tech:project_name": "codecommit-backup",
        "tech:source_repo_arn": repo_arn,
    }
    s3path.put_tags(tags=tags)

    print(f"preview backup of {repo_name!r} at: {s3path.console_url}")

    # clean up old backups
    s3dir = s3path.parent
    s3path_list = sorted(
        s3dir.iter_objects(),
        key=lambda s3path: s3path.last_modified_at,
        reverse=True,
    )

    if len(s3path_list) > keep_at_least:
        s3path: S3Path
        for s3path in s3path_list[3:]:
            if (now - s3path.last_modified_at).total_seconds() >= (
                retention_period * 24 * 60 * 60
            ):
                s3path.delete_if_exists()


if __name__ == "__main__":
    bsm = BotoSesManager()
    context.attach_boto_session(bsm.boto_ses)
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    for repo_name in repo_list:
        backup_one_repo(
            repo_name=repo_name,
        )
