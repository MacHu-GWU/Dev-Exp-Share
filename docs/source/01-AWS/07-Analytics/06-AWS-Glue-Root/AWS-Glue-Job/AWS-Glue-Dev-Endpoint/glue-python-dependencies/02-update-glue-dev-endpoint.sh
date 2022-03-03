#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_venv="${dir_here}/venv"
bin_pip="${dir_here}/venv/bin/pip"
path_requirements="${dir_here}/requirements.txt"
dir_site_packages="${dir_here}/site-packages"
path_site_packages_zip="${dir_here}/site-packages.zip"

bucket="aws-data-lab-sanhe-for-everything-us-east-2"
key="glue/artifacts/python-library/etl-job.zip"
dev_endpoint_name="sanhe-dev"

# pip install required dependenceis to site-packages directory
install_dependencies() {
    if [ -d "${dir_site_packages}" ] ; then
        rm -r "${dir_site_packages}"
    fi
    mkdir -p "${dir_site_packages}"
    pip install -t "${dir_site_packages}" -r "${path_requirements}"
}


# create site-packages.zip file from site-packages directory
create_zip_file() {
    if [ -f "${path_site_packages_zip}" ] ; then
        rm "${path_site_packages_zip}"
    fi
    cd "${dir_site_packages}"
    zip ""${path_site_packages_zip}"" * -r -9 -q -x __pycache__\* bin\* boto3\* botocore\* s3transfer\* setuptools\* pip\* wheel\* twine\* _pytest\* pytest\* numpy\* pandas\* pyarrow\*
}


# upload site-packages.zip to S3
upload_to_s3() {
    aws s3 cp "${path_site_packages_zip}" "s3://${bucket}/${key}"
}


# update glue dev endpoint python library
update_dev_endpoint() {
    aws glue update-dev-endpoint --endpoint-name "${dev_endpoint_name}" --custom-libraries ExtraPythonLibsS3Path="s3://${bucket}/${key}" --update-etl-libraries
}

# install_dependencies
# create_zip_file
# upload_to_s3
# update_dev_endpoint
