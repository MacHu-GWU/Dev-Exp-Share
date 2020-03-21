

快速查询:


.. list-table:: docker run
    :widths: 10 10 10
    :header-rows: 1

    * - Title
      - Command
      - Explain
    * - Run Image, Mount Volume in Background
      - .. code-block:: bash

            docker run -dt --name <identifier> --mount source=<vol-name>,target=<directory> <image>:<tag>
      -
    * - Title
      - .. code-block:: bash

            docker run -dt --name <identifier> --mount type=bin,source=<directory>,target=<directory> <image>:<tag>
      - Explain



.. list-table:: docker container
    :widths: 10 10 10
    :header-rows: 1

    * - Title
      - Command
      - Explain
    * - Value1
      - ``docker container start <identifier>``
      - Value3
    * - Value1
      - ``docker container stop <identifier>``
      - Value3
    * - Value1
      - ``docker container rm <identifier>``
      - Value3
    * - Value1
      - ``docker ps -a``
      - Value3

当 container 被 ``docker container stop <id>`` 关闭时, 如果不加 ``-rm`` 参数, container 是不会被从磁盘上真正删除的, 同时被这些未被删除的 container 所 mount 的 volume 也无法被 ``docker volumn rm <id>`` 所删除.

- 查看所有在本地的 container, 包括已停止的 (see all containers on the Docker host, including stopped containers): ``docker ps -a``
- 删除所有已经停止的 container (clean stopped container): ``docker container prune``

Reference: https://docs.docker.com/config/pruning/#prune-containers


挂载:


docker run -dt --name web --mount source=my-vol,target=/webapp ubuntu:18.04