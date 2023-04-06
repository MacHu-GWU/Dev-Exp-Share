Forum 应用, Postgresql 实现
------------------------------------------------------------------------------

板块, 用户, 贴子, 回复, 权限组,


board
    board_id, primary_key
    title
    description

user
    user_id, primary_key
    email
    password_digest
    create_at
    security_group_id

post
    post_id, primary_key
    nth, primary_key
    title
    content
    author_id
    create_at
    update_at
    board_id


security_group

    security_group_id, primary_key
    description


action

    action_id, primary_key
    description


security_group_action

    security_group_id, primary_key
    action_id, primary_key
