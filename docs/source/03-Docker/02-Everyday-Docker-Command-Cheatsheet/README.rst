Everyday Docker Command Cheatsheet
==============================================================================

Docker Command Line Reference: https://docs.docker.com/engine/reference/commandline/container/


Play with a new image
------------------------------------------------------------------------------

Found a new image, want to play with it?

.. list-table::
    :widths: 10 10 10
    :header-rows: 1

    * - Title
      - Command
      - Explain
    * - Run image in detached, terminal mode
      - .. code-block:: bash

            docker run --rm -dt --name <name> <image>:<tag>
      - Usually, you don't need volume / dir mount, and port mapping. ``--rm`` automatically remove it self at stopping.
    * - Enter the container
      - .. code-block:: bash

            docker exec -it <name> bash
      - Enter the container's terminal.
    * - Stop the container (auto remove)
      - .. code-block:: bash

            docker container stop <name>
      - That's why we need a name when ``run``.


List containers
------------------------------------------------------------------------------

.. list-table::
    :widths: 10 10 10
    :header-rows: 1

    * - Title
      - Command
      - Explain
    * - List Running Docker
      - .. code-block:: bash

          docker container ls

      - 列出所有运行中的容器
    * - List all container, include stopped
      - .. code-block:: bash

          docker ps -a

      - 列出所有的, 包括已经停止的容器
    * - Clean all unused image, release disk
      - .. code-block:: bash

          docker image prune

      - 清除所有没有被任何容器使用的镜像
    * - Delete all untagged images
      - .. code-block::

          docker rmi $(docker images -q --filter "dangling=true")
      - 清楚那些 tag 被覆盖掉后为 None 的镜像
    * - Clean all stopped container, release disk
      - .. code-block:: bash

          docker container prune

      - 清除所有已经停止的容器
    * - Search Running container by name
      - .. code-block:: bash

          docker container ls -a -f name=xxx
      -


# Delete all containers
docker rm $(docker ps -aq)
# Delete all images
docker rmi $(docker images -q)
# Delete all untagged images
docker rmi $(docker images -q --filter "dangling=true")