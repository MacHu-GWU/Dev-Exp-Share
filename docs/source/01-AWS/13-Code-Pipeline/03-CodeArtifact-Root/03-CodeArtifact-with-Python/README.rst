.. _aws-code-artifact-with-python:

AWS CodeArtifact with Python
==============================================================================
Keywords: AWS CodeArtifact, Code Artifact, Python

**将你的包发布到 Repo**

首先你要在本地先 build 好 distribution artifacts:

.. code-block:: bash

    python setup.py sdist bdist_wheel --universal

然后用 aws cli 对 CodeArtifact 进行身份验证, 并自动对 Python 的包发布工具 `twine <https://twine.readthedocs.io/en/stable/>`_ 进行配置, 这个本质就是获得一个 token 然后把这个 token 放在 twine 的配置文件 ``~/.pypirc`` 中.

.. code-block:: bash

    aws codeartifact login --tool twine --domain my_domain --domain-owner 111122223333 --repository my_repo

然后你就可以用 twine 将你的 artifacts 发布到你的私有 repo 里了:

.. code-block:: bash

    # 注意, 这个 codeartifact 是 aws cli 自动创建的 config profile, 请不要乱改
    twine upload --repository codeartifact dist/*

**从 Repo 上安装你已发布的包**

然后用 aws cli 对 CodeArtifact 进行身份验证, 并自动对 Python 的包管理 `pip <https://pip.pypa.io/en/stable/>`_ 进行配置, 这个本质就是获得一个 token 然后把这个 token 放在 pip 的配置文件 ``~/.config/pip/pip.conf`` 中.

.. code-block:: bash

    aws codeartifact login --tool pip --domain my_domain --domain-owner 111122223333 --repository my_repo

然后你就可以使用 ``pip install ...`` 命令了, pip 会优先到你的 repo 上去搜索, 搜不到才会去 public PyPI 上搜索.
