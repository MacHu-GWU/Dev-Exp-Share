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
        T.post_id,
        T.nth
    FROM (
        SELECT
            post.post_id,
            post.nth,
            max(post.create_at) as last_comment_create_at
        FROM post
        WHERE
            post.board_id = :board_id
            AND post.create_at >= :one_day_before_now
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
    ORDER BY post.create_time ASC
    SKIP 10
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
