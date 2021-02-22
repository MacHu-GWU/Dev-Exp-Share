#!/bin/bash

# Before playing with this script, open your terminal, manually ssh to the ec2, and verify the outcome::
#
# EC2_IP="111.111.111.111"
# ssh -i ~/ec2-pem/eq-sanhe-dev.pem "ec2-user@${EC2_IP}"

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
git_repo_name="Dev-Exp-Share"
dir_project_root="$(python -c "print('${dir_here}'.split('${git_repo_name}')[0] + 'Dev-Exp-Share')")"
source "${dir_project_root}/bin/py/python-env.sh"
dir_venv_bin="${dir_venv}/bin"
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# clean up last ansible run effect
rm ~/test.txt

# ping hosts
#${dir_venv_bin}/ansible all -i ${host_file} -m ping

# execute playbook
${dir_venv_bin}/ansible-playbook ${dir_here}/playbook.yml

# validate effect
cat ~/test.txt
