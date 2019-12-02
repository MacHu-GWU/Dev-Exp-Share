Deploy App to a container running on your local laptop
==============================================================================

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
    docker run --rm -dt --name my-app --mount type=bind,source=$dir_here,target=/opt/here -p 80:12345 python:3.6.8-slim

    # enter container
    docker exec -it my-app bash

    # run web app
    cd /opt/here
    pip install flask
    python app.py

It maps your localhost http port 80 to 12345 in container.

Open browswer http://localhost:80
