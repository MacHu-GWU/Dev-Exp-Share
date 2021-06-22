#!/bin/bash

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
tmp_lambda_deploy_folder="lambda-deploy"
tmp_lambda_deploy_file="lambda-deploy-package.zip"

# clear old temp dir
rm -r ${dir_here}/${tmp_lambda_deploy_folder} 2> /dev/null
rm ${dir_here}/${tmp_lambda_deploy_file} 2> /dev/null
mkdir ${dir_here}/${tmp_lambda_deploy_folder}

# build dependencies
pip install --requirement ${dir_here}/requirements.txt --prefix ${dir_here}/${tmp_lambda_deploy_folder} --ignore-installed

# copy lambda handler file
cp ${dir_here}/consumer.py ${dir_here}/${tmp_lambda_deploy_folder}/lib/python3.7/site-packages/consumer.py

# package everything
cd ${dir_here}/${tmp_lambda_deploy_folder}/lib/python3.7/site-packages
zip ${dir_here}/${tmp_lambda_deploy_file} * -r -9 -q -x boto3\* botocore\* s3transfer\* setuptools\* easy_install.py pip\* wheel\* twine\* _pytest\* pytest\*;
