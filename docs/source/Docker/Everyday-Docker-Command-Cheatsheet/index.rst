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

      -
    * - List all container, include stopped
      - .. code-block:: bash

          docker ps -a

      -
    * - Clean all stopped container, release disk
      - .. code-block:: bash

          docker container prune

      -
    * - Search Running container by name
      - .. code-block:: bash

          docker container ls -a -f name=xxx
      -
