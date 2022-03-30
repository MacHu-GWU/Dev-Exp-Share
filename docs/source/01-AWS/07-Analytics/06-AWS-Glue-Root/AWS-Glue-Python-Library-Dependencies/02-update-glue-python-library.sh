#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_site_packages="${dir_here}/site-packages"
path_site_packages_zip="${dir_here}/site-packages.zip"

#------------------------------------------------------------
# Update your configuration here, don't touch else where
#------------------------------------------------------------
# The python version you are using, for Glue 1.0 = 3.6, Glue 2.0/3.0 = 3.7
# Glue dev endpoint is Glue 1.0
python_ver="3.6"
dependency_layer_name="dynamodb_tracker"
bucket="aws-data-lab-sanhe-for-everything-us-east-2"
dev_endpoint_name="sanhe-dev"
glue_job_name="output-control"
#------------------------------------------------------------
bin_python="python${python_ver}"
bin_pip="pip${python_ver}"
requirements_file="python${python_ver}-${dependency_layer_name}-requirements.txt"
path_requirements="${dir_here}/${requirements_file}"
key="glue/artifacts/python-library/python${python_ver}-${dependency_layer_name}-requirements.zip"

# pip install required dependenceis to site-packages directory
install_dependencies() {
    if [ -d "${dir_site_packages}" ] ; then
        rm -r "${dir_site_packages}"
    fi
    mkdir -p "${dir_site_packages}"
    ${bin_pip} install -t "${dir_site_packages}" -r "${path_requirements}"
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

# update glue dev endpoint python library
# ref: https://docs.aws.amazon.com/cli/latest/reference/glue/update-dev-endpoint.html
update_dev_endpoint() {
    aws glue update-dev-endpoint --endpoint-name "${dev_endpoint_name}" --custom-libraries ExtraPythonLibsS3Path="s3://${bucket}/${key}" --update-etl-libraries
}

# update glue job python library
# ref: https://docs.aws.amazon.com/cli/latest/reference/glue/update-job.html
update_glue_job() {
    # aws glue update-job --job-name "${glue_job_name}" --job-update "Description=\"Hello Alice\""
    aws glue update-job --job-name "${glue_job_name}" --job-update "{\"Command\": {\"Name\": \"glueetl\"}, \"Role\": \"arn:aws:iam::669508176277:role/sanhe-glue-job-runner\", \"DefaultArguments\": {\"--extra-py-files\": \"s3://${bucket}/${key}\"}}"
}

# install_dependencies
# create_zip_file
# upload_to_s3
# update_dev_endpoint
# update_glue_job
