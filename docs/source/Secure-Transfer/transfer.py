# -*- coding: utf-8 -*-

import boto3
from pathlib_mate import Path
from windtalker import SymmetricCipher

class Config:
    PASSWORD = "password_here"
    AWS_PROFILE = "aws_profile_here"
    BUCKET = "s3_bucket_name"
    KEY = "s3_key"

p_source = Path(__file__).change(new_basename="test-data")
p_archive = p_source.change(new_basename="data-sender.zip")
p_encrypted_archive = p_archive.change(new_ext=".dat")
p_encrypted_archive_downloads = p_source.change(new_basename="data-receiver.dat")
p_archive_downloads = p_encrypted_archive_downloads.change(new_ext=".zip")

c = SymmetricCipher(password=Config.PASSWORD)
boto_ses = boto3.session.Session(profile_name=Config.AWS_PROFILE)
s3_client = boto_ses.client("s3")

def upload():
    p_source.make_zip_archive(dst=p_archive, overwrite=True)
    c.encrypt_file(p_archive.abspath, output_path=p_encrypted_archive.abspath, overwrite=True)
    s3_client.upload_file(p_encrypted_archive.abspath, Config.BUCKET, Config.KEY)

def download():
    s3_client.download_file(Config.BUCKET, Config.KEY, p_encrypted_archive_downloads.abspath)
    c.decrypt_file(p_encrypted_archive_downloads.abspath, p_archive_downloads.abspath)

if __name__ == "__main__":
    # upload()
    # download()
    pass