.. _jq:

jq Cheat Sheet
==============================================================================

jq 是一个强大的 JSON Query 命令行工具, 可以对 JSON 进行各种各样简单或复杂的操作. 当然 Linux 下用 Python 对 JSON 进行复杂的操作更容易, 对人类更友好. 但是 jq 作为高阶工具, 学会了能用简单的语法完成 90% 的操作.

.. contents::
    :local:


Access a Value
------------------------------------------------------------------------------

.. code-block:: python

    {
        "name": "Alice",
        "profile": {
            "ssn": "1234-56-789",
            "numbers": [
                0, 1, 2
            ]
        }
    }

.. code-block:: bash

    $ cat data.json | jq '.name'
    "Alice"

    $ cat data.json | jq '.name' -r
    Alice

    $ cat data.json | jq '.name.profile' -r
    1234-56-789

    $ cat data.json | jq '.profile.numbers[0]' -r
    0

    $ cat data.json | jq '.profile.numbers[1]' -r
    1

.. code-block:: python

    [
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        },
        {
            "id": 1,
            "name": "Cathy"
        }
    ]

.. code-block:: bash

    $ cat data.json | jq '.[0]' -r
    {
      "id": 1,
      "name": "Alice"
    }


SELECT
------------------------------------------------------------------------------

.. code-block:: python

    [
        1,
        2,
        3
    ]


.. code-block:: bash

    $ cat data.json | jq 'map(select(. == 1))' -r
    [
        1
    ]


.. code-block:: python

    [
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        },
        {
            "id": 3,
            "name": "Cathy"
        }
    ]


.. code-block:: bash

    $ cat data.json | jq 'map(select(.id == 1))[0].name' -r
    Alice


.. code-block:: python

    {
        "data": [
            {
                "id": 1,
                "name": "Alice"
            },
            {
                "id": 2,
                "name": "Bob"
            },
            {
                "id": 3,
                "name": "Cathy"
            }
        ]
    }


.. code-block:: bash

    $ cat data.json | jq '.data | map(select(.id == 1))[0].name' -r
    Alice


String Interpolation
------------------------------------------------------------------------------

.. code-block:: python

    [
        {
            "id": 1,
            "firstname": "Obama",
            "lastname": "Barrack"
        },
        {
            "id": 2,
            "firstname": "Trump",
            "lastname": "Donald"
        }
    ]


.. code-block:: bash

    $ cat data.json | jq '[ { "fullname": .[] | "\(.firstname) \(.lastname)" } ]'
    [
        {
            "fullname": "Obama Barrack"
        },
        {
            "fullname": "Trump Donald"
        }
    ]
