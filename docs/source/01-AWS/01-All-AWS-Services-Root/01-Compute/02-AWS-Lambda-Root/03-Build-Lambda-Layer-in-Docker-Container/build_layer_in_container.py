# -*- coding: utf-8 -*-

"""
This shell script can build AWS Lambda Python Layer in AWS SAM CI/CD docker images
see https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html.

This script is based on this official document:

- How do I create a Lambda layer using a simulated Lambda environment with Docker?: https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/
"""

import os
import glob
import shutil
import subprocess
from pathlib import Path

python_version = "3.6" # <===== change the python version here, then you are done


def get_os_user() -> str:
    return subprocess.run(
        ["id", "-u"],
        capture_output=True,
    ).stdout.decode("utf-8").strip()


def get_os_user_group() -> str:
    return subprocess.run(
        ["id", "-g"],
        capture_output=True,
    ).stdout.decode("utf-8").strip()

# locate important dir and file
dir_here = Path(__file__).absolute().parent
dir_project_root = dir_here

path_requirements = dir_project_root / "requirements.txt"
dir_build_lambda_layer = dir_project_root / "build" / "lambda" / "layer"
dir_build_lambda_layer.mkdir(parents=True, exist_ok=True)

dir_python = dir_build_lambda_layer / "python"
path_layer_zip = dir_build_lambda_layer / "layer.zip"

# preprocess the python_version string
python_version = python_version.lower()
if "python" in python_version:
    python_version.replace("python", "")

# See https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html
ecr_uri = f"public.ecr.aws/sam/build-python{python_version}"

print(f"Build AWS Lambda Layer for python{python_version}")
print(f"  use docker image {ecr_uri}")

# See https://vsupalov.com/docker-shared-permissions/
# and https://stackoverflow.com/questions/42423999/cant-delete-file-created-via-docker
print("  get current OS user and user group info")
user = get_os_user()
user_group = get_os_user_group()
args = [
    "docker", "run", "-v", f"{dir_project_root}:/var/task", "--user", f"{user}:{user_group}", ecr_uri,
    "/bin/sh", "-c",
    f"pip install -r /var/task/requirements.txt -t /var/task/build/lambda/layer/python/"
]

print("  clean up existing 'python/' folder and 'layer.zip' file")
if dir_python.exists():
    shutil.rmtree(f"{dir_python}")
if path_layer_zip.exists():
    path_layer_zip.unlink()

print("  build lambda layer in docker container ...")
subprocess.run(args)

print("  zip the 'layer.zip' file")
cwd = os.getcwd() # get the current dir, and revert it back later
os.chdir(f"{dir_build_lambda_layer}")
ignore_package_list = [
    "boto3",
    "botocore",
    "s3transfer",
    "setuptools",
    "pip",
    "wheel",
    "twine",
    "_pytest",
    "pytest",
]
args = (
    [
        "zip", f"{path_layer_zip}",
        "-r", "-9", "-q",
    ]
    + glob.glob("*")
    + ["-x", ]
)
for package in ignore_package_list:
    args.append(f"python/{package}*")
subprocess.run(args)

os.chdir(cwd) # revert it back to original dir
print(f"  done! check the '{path_layer_zip}' file.")