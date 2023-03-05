#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
this script injects temp AWS credential received from aws sts into
~/.aws/credentials and ~/.aws/config file.
"""

import os

HOME = os.path.expanduser("~")

AWS_DIR = os.path.join(HOME, ".aws")
CREDENTIAL_FILE = os.path.join(AWS_DIR, "credentials")
CONFIG_FILE = os.path.join(AWS_DIR, "config")


def read_text(abspath, encoding="utf-8"):
    with open(abspath, "rb") as f:
        return f.read().decode(encoding)


def write_text(text, abspath, encoding="utf-8"):
    with open(abspath, "wb") as f:
        return f.write(text.encode(encoding))


def ensure_aws_configured_exists():
    if not os.path.exists(AWS_DIR):
        os.mkdir(AWS_DIR)
    if not os.path.exists(CREDENTIAL_FILE):
        write_text("", CREDENTIAL_FILE)
    if not os.path.exists(CONFIG_FILE):
        write_text("", CONFIG_FILE)


ensure_aws_configured_exists()


def update_aws_profile(original_profile_name,
                       access_key_id,
                       secret_access_key,
                       session_token,
                       aws_region,
                       delimiter="_"):
    access_key_id_line = "aws_access_key_id = {}".format(access_key_id)
    secret_access_key_line = "aws_secret_access_key = {}".format(secret_access_key)
    session_token_line = "aws_session_token = {}".format(session_token)

    region_line = "region = {}".format(aws_region)
    output_line = "output = json"

    new_profile_name = "{}{}mfa".format(original_profile_name, delimiter)

    # work on credentials file
    cred_lines = [
        line.strip()
        for line in read_text(CREDENTIAL_FILE).split("\n")
    ]

    new_profile_name_stub = "[{}]".format(new_profile_name)
    if new_profile_name_stub in cred_lines:
        ind = cred_lines.index(new_profile_name_stub)
        cred_lines[ind + 1] = access_key_id_line
        cred_lines[ind + 2] = secret_access_key_line
        cred_lines[ind + 3] = session_token_line
    else:
        cred_lines.extend([
            "",
            new_profile_name_stub,
            access_key_id_line,
            secret_access_key_line,
            session_token_line,
        ])

    write_text("\n".join(cred_lines), CREDENTIAL_FILE)

    # work on config file
    config_lines = [
        line.strip()
        for line in read_text(CONFIG_FILE).split("\n")
    ]

    new_profile_name_stub = "[profile {}]".format(new_profile_name)
    if new_profile_name_stub in config_lines:
        ind = config_lines.index(new_profile_name_stub)
        config_lines[ind + 1] = region_line
        config_lines[ind + 2] = output_line
    else:
        config_lines.extend([
            "",
            new_profile_name_stub,
            region_line,
            output_line,
        ])

    write_text("\n".join(config_lines), CONFIG_FILE)


if __name__ == "__main__":
    import sys

    original_profile_name = sys.argv[1]
    access_key_id = sys.argv[2]
    secret_access_key = sys.argv[3]
    session_token = sys.argv[4]
    aws_region = sys.argv[5]

    update_aws_profile(
        original_profile_name=original_profile_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        aws_region=aws_region
    )


    def test():
        update_aws_profile(
            original_profile_name="eq_cms",
            access_key_id="AAAA",
            secret_access_key="BBBB",
            session_token="CCCC",
            aws_region="us-east-1"
        )
