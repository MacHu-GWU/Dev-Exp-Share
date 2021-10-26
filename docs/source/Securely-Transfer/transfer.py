# -*- coding: utf-8 -*-

"""
make a zip archive for a folder, encrypt it and upload to AWS S3.
then download it from AWS S3 on another machine and decrypt it.

pip install pathlib_mate
pip install windtalker
pip install boto3
"""

import boto3
from pathlib_mate import Path
from windtalker import SymmetricCipher


class Config:
    PASSWORD = "password_here"  # the password you use to encrypt the file
    AWS_PROFILE = "aws_profile_here"  # aws profile
    BUCKET = "s3_bucket_name"
    KEY = "s3_key"


p_source = Path(__file__).change(new_basename="test-data") # the folder you want to upload
p_archive = p_source.change(new_basename="data-sender.zip") # the temp archive file
p_encrypted_archive = p_archive.change(new_basename="data-sender.dat") # the temp encrypted data file
p_encrypted_archive_downloads = p_source.change(new_basename="data-receiver.dat") # the temp encrypted data file
p_archive_downloads = p_encrypted_archive_downloads.change(new_basename="data-receiver.zip") # the temp decrypted data archive

c = SymmetricCipher(password=Config.PASSWORD)
boto_ses = boto3.session.Session(profile_name=Config.AWS_PROFILE)
s3_client = boto_ses.client("s3")


def upload():
    p_source.make_zip_archive(dst=p_archive, overwrite=True)
    c.encrypt_file(p_archive.abspath, output_path=p_encrypted_archive.abspath, overwrite=True)
    with open(p_encrypted_archive.abspath, "rb") as f:
        s3_client.put_object(Bucket=Config.BUCKET, Key=Config.KEY, Body=f.read())


def download():
    response = s3_client.get_object(Bucket=Config.BUCKET, Key=Config.KEY)
    with open(p_encrypted_archive_downloads.abspath, "wb") as f:
        f.write(response["Body"].read())
    c.decrypt_file(p_encrypted_archive_downloads.abspath, p_archive_downloads.abspath)


if __name__ == "__main__":
    # upload()
    # download()
    pass
