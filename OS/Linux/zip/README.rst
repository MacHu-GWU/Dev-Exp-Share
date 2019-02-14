``zip``
==============================================================================


Test directory::

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


Assuming that, current directory is ``requests-project``.


Compress entire folder, include the folder itself
------------------------------------------------------------------------------

.. code-block:: bash

    $ cd ${ROOT}
    $ cd ..
    $ zip requests-project.zip requests-project -r

content of ``requests-project.zip``::

    |---requests-project
        |--- requests
            |--- utils
                |--- __init__.py
            |--- __init__.py
            |--- api.py
            |--- response.py
        |--- MakeFile
        |--- README.txt


Compress entire folder, exclude the folder it self
------------------------------------------------------------------------------

.. code-block:: bash

    $ cd ${ROOT}
    $ zip ../requests-project.zip * -r


content of ``requests-project.zip``::

    |--- requests
        |--- utils
            |--- __init__.py
        |--- __init__.py
        |--- api.py
        |--- response.py
    |--- MakeFile
    |--- README.txt


Frequently Used Options
------------------------------------------------------------------------------

- include these only: ``-i *.py *.txt *.rst``
- exclude theses: ``-x *.zip *.json *.pk``

Becareful with ``*``, sometime you need to add escape char ``\`` before that. For example:

- exclude ``.json`` file: ``zip mydir.zip mydir -r -x \*.json``
- exclude the ``pip`` folder: ``zip site-package.zip site-package -r -x pip\*``