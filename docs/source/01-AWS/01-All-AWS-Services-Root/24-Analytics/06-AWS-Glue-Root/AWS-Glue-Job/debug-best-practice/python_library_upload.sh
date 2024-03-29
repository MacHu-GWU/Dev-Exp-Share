#!/bin/bash

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"

pip install -r "${dir_here}/requirements.txt" --target="${dir_here}/site-packages"

cd "${dir_here}/site-packages"
zip "${dir_here}/site-packages.zip" * -r -9 -q -x __pycache__\* botocore\* boto3\* dateutil\* jmespath\* urllib3\* bin\* six.py;

aws s3 cp "${dir_here}/site-packages.zip" s3://aws-data-lab-sanhe-for-everything/artifacts/glue_job_python_library/debug-best-practice-site-packages.zip
