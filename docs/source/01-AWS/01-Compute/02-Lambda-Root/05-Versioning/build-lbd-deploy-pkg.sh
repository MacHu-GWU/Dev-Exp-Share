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
# copy source code
cp ${dir_here}/lbd_handler.py ${dir_here}/${tmp_lambda_deploy_folder}/lib/python3.6/site-packages/lbd_handler.py

# package everything
cd ${dir_here}/${tmp_lambda_deploy_folder}/lib/python3.6/site-packages
zip ${dir_here}/${tmp_lambda_deploy_file} * -r -9 -q -x boto3\* botocore\* s3transfer\* setuptools\* easy_install.py pip\* wheel\* twine\* _pytest\* pytest\*

# upload to s3
md5_hash="$(python ${dir_here}/md5.py ${dir_here}/${tmp_lambda_deploy_file})"
aws s3 cp ${dir_here}/${tmp_lambda_deploy_file} s3://sanhe-admin-for-everything/lambda/MacHu-GWU/lbd-versioning/${md5_hash}.zip --profile sanhe
