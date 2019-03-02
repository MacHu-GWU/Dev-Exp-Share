#!/bin/bash
# -*- coding: utf-8 -*-

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
dir_bin="$(dirname "${dir_here}")"
dir_project_root=$(dirname "${dir_bin}")

source ${dir_bin}/py/python-env.sh

print_colored_line $color_cyan "[DOING] print useful information:"
if [ -e ${dir_venv} ]; then
    print_colored_line $color_green "virtualenv is ready to use at: ${dir_venv}"
else
    print_colored_line $color_red "virtualenv are NOT found at: ${dir_venv}"
fi

if [ -z "$(${bin_pip} show ${package_name} | grep "Name:")" ]; then
    print_colored_line $color_red "${package_name} is NOT installed at: ${dir_venv_site_packages}"
else
    print_colored_line $color_green "${package_name} is installed at: ${dir_venv_site_packages}"
fi

print_colored_ref_line ${color_cyan} "venv" ${dir_venv}
print_colored_ref_line ${color_cyan} "python executable" ${bin_python}
print_colored_ref_line ${color_cyan} "pip executable" ${bin_pip}
print_colored_ref_line ${color_cyan} "site-packages" ${dir_venv_site_packages}
print_colored_ref_line ${color_cyan} "site-packages64" ${dir_venv_site_packages64}
print_colored_ref_line ${color_cyan} "local html doc" ${path_sphinx_index_html}
print_colored_ref_line ${color_cyan} "readme file" ${path_readme}
print_colored_ref_line ${color_cyan} "versioned doc on s3" ${s3_uri_doc_versioned}
print_colored_ref_line ${color_cyan} "latest doc on s3" ${s3_uri_doc_latest}
print_colored_ref_line ${color_cyan} "latest doc on readthedocs.org" ${rtd_url}
