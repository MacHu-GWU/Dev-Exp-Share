Distribute Python Package
==============================================================================
Keywords:

本文写于 2023-05-22.

本文介绍了如何将你的 Python 包打包发布到 PyPI 上. 以及相关的工具.

Python 社区早期 (2020 年以前) 都是用 setuptools + setup.py 文件来管理发布的. 而从 2020 年以后, pyproject.toml 逐渐变得流行并且以后 pip 将会只支持 pyproject.toml 文件. 社区官方的打包工具也从 setuptools 是变成了 build.

.. code-block:: bash

    # 早期
    ``python setup.py sdist``

    # 现在
    ``python -m build --sdist --wheel``

- `Build <https://pypa-build.readthedocs.io/en/stable/>`_
- `Twine <https://twine.readthedocs.io/en/stable/>`_