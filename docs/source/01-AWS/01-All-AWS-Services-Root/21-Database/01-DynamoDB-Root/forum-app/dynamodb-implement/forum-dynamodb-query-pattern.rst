find user_id by email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    res = query(user-email-index.email=:email)
    return res.items[0].user_id


find 10 most recent commented post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        T.post_id
    FROM (
        SELECT
            comment.post_id
            max(comment.create_at) as last_comment_create_at
        FROM comment
        WHERE
            comment.create_at >= :one_day_before_now
        GROUP BY comment.post_id
    ) T
    ORDER BY T.last_comment_create_at DESC
    LIMIT 10


find all comment of a post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    -- page 2
    SELECT *
    FROM post
    WHERE post.post_id = :post_id
    ORDER BY post.nth ASC
    SKIP 10
    LIMIT 10


find all actions can be done by a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        security_group.action_id_list
    FROM security_group_and_action
    WHERE
        security_group.security_group_id = :security_group_id



find all post published by a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        post-author_id-post_id.post_id
    FROM post-author_id-post_id
    WHERE post-author_id-post_id.author_id = :user_id
    ORDER BY post-author_id-post_id.create_at DESC
