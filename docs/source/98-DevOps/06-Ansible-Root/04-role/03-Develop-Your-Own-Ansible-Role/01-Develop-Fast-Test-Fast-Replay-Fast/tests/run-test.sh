#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$( dirname $( dirname $(dirname $( dirname $( dirname $( dirname $( dirname $( dirname ${dir_here}))))))))"

echo ${dir_project_root} # the path should end with Dev-Exp-Share

source "${dir_project_root}/bin/py/python-env.sh"

dir_venv_bin="${dir_venv}/bin"
dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${dir_venv_bin}/ansible-playbook ${dir_here}/playbook.yml --extra-vars "role_dir=$( dirname ${dir_here} )"
