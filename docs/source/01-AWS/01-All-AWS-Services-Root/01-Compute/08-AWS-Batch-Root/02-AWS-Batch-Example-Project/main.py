# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context


def copy_s3_folder(
    bsm: BotoSesManager,
    s3dir_source: S3Path,
    s3dir_target: S3Path,
):
    """
    Core logic.
    """
    context.attach_boto_session(bsm.boto_ses)
    print(f"copy files from {s3dir_source.uri} to {s3dir_target.uri}")
    for s3path_source in s3dir_source.iter_objects():
        relpath = s3path_source.relative_to(s3dir_source)
        s3path_target = s3dir_target.joinpath(relpath)
        print(f"copy: {relpath.key}")
        s3path_source.copy_to(s3path_target, overwrite=True)


def main(
    region: str,
    s3uri_source: str,
    s3uri_target: str,
):
    """
    wrapper around the core logic, expose the parameter to CLI.
    """
    print(f"received: region = {region!r}, s3uri_source = {s3uri_source!r}, s3uri_target = {s3uri_target!r}")
    copy_s3_folder(
        bsm=BotoSesManager(region_name=region),
        s3dir_source=S3Path(s3uri_source).to_dir(),
        s3dir_target=S3Path(s3uri_target).to_dir(),
    )


# convert the app to a CLI app.
if __name__ == "__main__":
    import fire

    fire.Fire(main)
