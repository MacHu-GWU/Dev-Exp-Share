Build Your Own Docker Image
==============================================================================

一个 ``Dockerfile`` 定义了 基础镜像, 以及从基础镜像到最终镜像的命令, 也就是说一个 Dockerfile 唯一决定了一个最终镜像的状态. 下面的命令常被用来构建一个 Docker Image, 命令的含义是, 在 ``.`` (当前路径, 当然你也可以指定其他路径, 比如 ``~/Github/my-docker-hub-repo``) 目录下寻找 ``Dockerfile`` 并将构建好的镜像打上 ``sanhe/learn-python:0.0.1`` 的标签

.. code-block:: bash

    docker build -t sanhe/learn-python:0.0.1 .


.. code-block:: bash

    docker push sanhe/learn-python:0.0.1
