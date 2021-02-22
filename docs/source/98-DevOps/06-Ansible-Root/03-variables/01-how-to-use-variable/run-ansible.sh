#!/bin/bash

# Before playing with this script, open your terminal, manually ssh to the ec2, and verify the outcome::

EC2_IP="111.111.111.111"
ssh -i ~/ec2-pem/eq-sanhe-dev.pem "ec2-user@${EC2_IP}"

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$( dirname $( dirname $( dirname $( dirname $( dirname $( dirname ${dir_here}))))))"

echo "dir_project_root=\"${dir_project_root}\"" # ends with Dev-Exp-Share

source "${dir_project_root}/bin/py/python-env.sh"

dir_venv_bin="${dir_venv}/bin"
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

host_file="${dir_here}/inventory.yml"

# ping hosts
${dir_venv_bin}/ansible all -i ${host_file} -m ping

# executte playbook
${dir_venv_bin}/ansible-playbook -i ${host_file} ${dir_here}/playbook.yml --extra-vars "@${dir_here}/vars.yml"
