Linux Command
==============================================================================


``zip``
------------------------------------------------------------------------------

::

    ROOT="requests-project"

    ${ROOT}
    |--- requests
        |--- utils
            |--- __init__.py
        |--- __init__.py
        |--- api.py
        |--- response.py
    |--- MakeFile
    |--- README.txt

- ``zip -r {output-filename} {filelist}``
- ``zip requests.zip requests -r``: compress requests folder, recursively.


Get:

.. code-block:: bash

    # create requests-project.zip next to requests-project dir
    $ cd requests
    $ zip ../requests.zip filelist

content of ``requests-project.zip``::

    |--- requests
        |--- utils
            |--- __init__.py
        |--- __init__.py
        |--- api.py
        |--- response.py
    |--- MakeFile
    |--- README.txt



::

    ${ZipFile}
    |--- utils
        |--- __init__.py
    |--- __init__.py
    |--- api.py
    |--- response.py

