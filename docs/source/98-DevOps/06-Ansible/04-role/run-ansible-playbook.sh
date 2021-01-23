#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$( dirname $( dirname $( dirname $( dirname $( dirname ${dir_here})))))"

echo ${dir_project_root} # the path should end with Dev-Exp-Share

source "${dir_project_root}/bin/py/python-env.sh"

dir_venv_bin="${dir_venv}/bin"
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${bin_python} ${dir_here}/pre_task_prepare_vars.py
#${dir_venv_bin}/ansible-playbook -i ${dir_here}/host.yml ${dir_here}/playbook.yml --extra-vars "@${dir_here}/vars.json"
${dir_venv_bin}/ansible-playbook ${dir_here}/playbook.yml --extra-vars "@${dir_here}/vars.json"