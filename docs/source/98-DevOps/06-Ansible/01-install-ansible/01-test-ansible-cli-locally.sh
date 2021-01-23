#!/bin/bash

# 使用 virtualenv 环境中的 ansible 命令行
# ansible 有好几个子命令, 详细列表请参考: https://docs.ansible.com/ansible/latest/user_guide/command_line_tools.html

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$( dirname $( dirname $( dirname $( dirname $( dirname ${dir_here})))))"
echo ${dir_project_root} # ends with Dev-Exp-Share
source "${dir_project_root}/bin/py/python-env.sh"

dir_venv_bin="${dir_venv}/bin"
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"ansible="${dir_venv_bin}/ansible"

${dir_venv_bin}/ansible
#${dir_venv_bin}/ansible-config
#${dir_venv_bin}/ansible-doc
#${dir_venv_bin}/ansible-inventory
#${dir_venv_bin}/ansible-playbook
