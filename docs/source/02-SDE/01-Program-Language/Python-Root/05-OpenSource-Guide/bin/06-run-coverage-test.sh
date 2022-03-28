#!/bin/bash
# Run code coverage test

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$(dirname "${dir_here}")"
dir_pytest_cache="${dir_project_root}/.pytest_cache"
dir_coverage_html="${dir_project_root}/htmlcov"

python_lib_name="s3bridge"

# if a file/dir exists, then remove it. do nothing if not exists.
# usage:
#
#   rm_if_exists "/tmp/downloads"
#   rm_if_exists "/tmp/test.txt"
rm_if_exists() {
    if [ -e $1 ]; then
        if [ -d $1 ]; then
            rm -r $1
        elif [ -f $1 ]; then
            rm $1
        fi
    fi
}

# remove existing coverage annotate
rm_if_exists "${dir_pytest_cache}"
rm_if_exists "${dir_coverage_html}"

# execute code coverage test
cd "${dir_project_root}" || return
${dir_project_root}/venv/bin/pytest "${dir_project_root}/tests" -s "--cov=${python_lib_name}" "--cov-report" "term-missing" "--cov-report" "html:${dir_coverage_html}"
