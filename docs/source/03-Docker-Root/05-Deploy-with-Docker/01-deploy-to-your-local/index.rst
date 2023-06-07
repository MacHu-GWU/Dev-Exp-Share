Deploy App to a container running on your local laptop
==============================================================================

.. contents::
    :depth: 1
    :local:


Manually run web server from scratch
------------------------------------------------------------------------------

- we quickly launch a base python image
- install flask
- prepare app.py file
- run web server and expose a port

content of ``app.py``:

.. code-block:: python

    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello world!"

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=12345, debug=True)

Run following commands:

.. code-block:: bash

    # cd to this dir
    cd <to-path-this-dir>

    # get absolute path of this dir
    dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

    # map this dir on local machine to ``/opt/here`` on container
    docker run --rm -dt --name my-app --mount type=bind,source=$dir_here,target=/var/app -p 80:12345 python:3.6.8-slim

    # enter container
    docker exec -it my-app bash

    # run web app
    cd /var/app
    pip install flask
    python app.py

It maps your localhost http port 80 to 12345 in container.

Open browswer http://localhost:80 see if it works.


Run docker container as a Command
------------------------------------------------------------------------------

In this tutorial, we will build a docker image that automatically run the web server when you run the container.

content of ``Dockerfile``:

.. code-block:: bash

    FROM python:3.6.8-slim
    RUN pip install flask
    COPY app.py /var/app/
    ENTRYPOINT ["python", "/var/app/app.py"]

Build the docker image, give it a name ``my-app:1``

.. code-block:: bash

    docker build -t my-app:1 .

Run docker as a command:

.. code-block:: bash

    docker run --rm -dt --name my-app -p 80:12345 my-app:1
