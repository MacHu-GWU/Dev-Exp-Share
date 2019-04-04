find user_id by email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT user.user_id
    FROM user
    WHERE user.email = :email


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

    SELECT *
    FROM comment
    WHERE comment.post_id = :post_id
    ORDER BY comment.comment_id ASC
    SKIP 100
    LIMIT 10


find all actions can be done by a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        security_group_and_action.action_id
    FROM security_group_and_action
    WHERE
        security_group_and_action.security_group_id = (
            SELECT users.security_group_id
            FROM users
            WHERE users.user_id = :user_id
        )


find all post published by a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: SQL

    SELECT
        post.post_id
    FROM post
    WHERE post.author_id = :user_id
    ORDER BY post.create_at DESC
