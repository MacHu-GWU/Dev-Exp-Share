# -*- coding: utf-8 -*-

"""
A simple automation script that can create the ``choices.xml`` file for
aws cli v2 installation. The documentation can be found:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
MacOS section, Command line - current user section, step 1.
"""

import os

dir_here = os.path.dirname(os.path.abspath(__file__))
dir_home = os.path.expanduser("~")
path_choices_templates_xml = os.path.join(dir_here, "choices_template.xml")
path_choices_xml = os.path.join(dir_here, "choices.xml")

with open(path_choices_templates_xml, "r") as f:
    tpl = f.read()
    content = tpl.format(USER_HOME=dir_home)
    with open(path_choices_xml, "w") as f:
        f.write(content)
