DynamoDB 实现 论坛 应用
==============================================================================




Postgresql 实现
------------------------------------------------------------------------------

板块, 用户, 贴子, 回复, 权限组


Board
    board_id
    title
    description

User
    user_id
    email
    password_digest
    create_at
    security_group_id

Post
    post_id
    title
    content
    author_id
    create_at
    update_at

Comment
    post_id
    comment_id
    user_id
    body
    create_at
    update_at

SecurityGroup

    security_group_id
    description

Action

    action_id
    description

SecurityGroupAction

    security_group_id
    action_id


MongoDB 实现
