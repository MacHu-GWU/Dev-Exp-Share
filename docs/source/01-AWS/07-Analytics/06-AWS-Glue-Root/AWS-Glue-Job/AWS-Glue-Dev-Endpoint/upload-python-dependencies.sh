#!/bin/bash
# Build AWS Lambda layer locally using current OS

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_site_packages="${dir_here}/site-packages"
path_site_packages_zip="${dir_here}/site-packages.zip"

# install dependencies
rm -r "${dir_site_packages}"
mkdir -p "${dir_site_packages}"
pip install -t "${dir_site_packages}" -r "${dir_here}/requirements.txt"

# create zip file
rm "${path_site_packages_zip}"
cd "${dir_site_packages}" && exit 1
zip ""${path_site_packages_zip}"" * -r -9 -q -x __pycache__\* boto3\* botocore\* s3transfer\* setuptools\* pip\* wheel\* twine\* _pytest\* pytest\*

# upload python library
bucket="aws-data-lab-sanhe-for-everything-us-east-2"
key="glue/artifacts/python-library/etl-job.zip"
aws s3 cp "${path_site_packages_zip}" s3://${bucket}/${key}
