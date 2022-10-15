# -*- coding: utf-8 -*-

"""
Manage Determinative Python Dependencies 管理 Python 依赖
==============================================================================
传统的 Python ``requirements.txt`` 文件有个问题就是里面的依赖可能会互相冲突, 特别是依赖的依赖之间互相冲突. 这会导致在不同的机器上不同的时间安装依赖会导致不同的结果. Python 社区有个项目 `poetry <https://python-poetry.org/>`_ 实现了determinative dependency management, 是的你在不同的机器, 不同时间, 安装的环境永远是一摸一样的.

但是我们这个项目没有那么 fancy, 我还是用的 `pygitrepo 0.0.7 <https://pypi.org/project/pygitrepo/>`_ 我自己开发的 Python 工作流软件配置的环境. 我们用一些比较笨但是有效的方法实现了类似的功能, 所以有必要做出一些说明.


如何 determinative dependency management
------------------------------------------------------------------------------
``**``requirements-main.txt`` 这个文件里记录了我们的代码中凡是真正需要 import 的包. 当然这些包会依赖其他包. 每次我们重新创建一个 venv 环境, 然后安装这些包, 然后将所有依赖的固定版本用 ``pip freeze`` 命令导出, 最后运行单元测试测试一下, 如果通过说明这个依赖是可以用的. 具体步骤如下.

1. 确保你是在 wotlk_private_server-project 跟目录下::

    pwd

2. 创建空的虚拟环境::

    pgr venv-remove
    pgr venv-up

3. 如果 ``requirements.txt`` 已经存在, 将已有的进行备份::

    cp requirements.txt requirements-backup.txt

4. 将 ``requirements-main.txt`` 中的内容拷贝到 ``requirements.txt`` 中::

    cp requirements-main.txt requirements.txt

5. 安装 ``requirements-main.txt`` 中的依赖::

    pgr pip-dev-install

6. 将已安装的依赖导出, 记得要删除 ``-e`` 开头的那一行. 那一行是该项目本身, 不属于依赖的一部分::

    $(pgr get-value dir_venv)/bin/pip freeze > requirements.txt

7. 运行单元测试, 如果出现了错误, 请修改 ``requirements-main.txt`` 文件, 并重新从 1-7 来一遍::

    pgr test

8. 如果成功意味着可以将 ``requirements.txt`` commit 到 Git 中了.


自动化脚本
------------------------------------------------------------------------------
我们有一个自动化脚本自动化了以上的全过程, 在 ``./bin/resolve_requirements.py`` 这个地方. 这个脚本本身只需要 Python3.6+ 标准库, 无需任何依赖 (当然你要提前装好 pygitrepo).
"""

import os
import shutil
import datetime
import subprocess
from pathlib import Path

py_ver = "3.8" # <=== update the python version you are trying to use

if "python" in py_ver:
    py_ver.replace("python", "")

dir_project_root = Path(__file__).absolute().parent
dir_venv = dir_project_root / ".venv-for-req"
path_pip = dir_venv / "bin" / "pip"

now = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")

path_requirements = dir_project_root / "requirements.txt"
path_requirements_main = dir_project_root / "requirements-main.txt"
path_requirements_backup = dir_project_root / f"requirements-backup-{now}.txt"


def s1_cd_to_project_root():
    os.chdir(f"{dir_project_root}")


def s2_create_virtualenv():
    """
    Create the temp virtual environment.
    """
    subprocess.run(["virtualenv", "-p", f"python{py_ver}", f"{dir_venv}"])


def s3_pip_install():
    """
    Pip install dependencies in requirements-main.txt file/
    """
    path_requirements_backup.write_text(path_requirements.read_text())
    subprocess.run([f"{path_pip}", "install", "-r", f"{path_requirements_main}"])


def s4_pip_freeze():
    """
    Export all installed dependencies with determinative version.
    """
    output = subprocess.run(
        [f"{path_pip}", "freeze"],
        capture_output=True,
    ).stdout.decode("utf-8")
    path_requirements.write_text(output)


def s5_delete_virtualenv():
    """
    Delete the temp virtual environment.
    """
    shutil.rmtree(f"{dir_venv}")


def run():
    s1_cd_to_project_root()
    s2_create_virtualenv()
    s3_pip_install()
    s4_pip_freeze()
    s5_delete_virtualenv()


if __name__ == "__main__":
    run()
