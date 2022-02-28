AWS Athena SQL - flattening nested arrays
==============================================================================

posts::

    post_id	    create_time     tags
    1			2000-01-01      [tag1, tag2, tag3]


.. code-block:: SQL

    SELECT
        t.post_id,
        tag
    FROM posts t
    CROSS JOIN UNNEST(t.tags) as t(tag)

output::

    post_id     tag
    1           tag1
    1           tag2
    1           tag3

解释:

.. code-block:: SQL

    SELECT *
    FROM posts t
    CROSS JOIN UNNEST(t.tags) as t(tag)

output::

    post_id     create_time     tag
    1           2000-01-01      tag1
    1           2000-01-01      tag2
    1           2000-01-01      tag3
