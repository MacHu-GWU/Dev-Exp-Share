Forum 应用, Postgresql 实现
------------------------------------------------------------------------------

板块, 用户, 贴子, 回复, 权限组,


user
    user_id, primary_key, partition_key
    email
    password_digest
    create_at
    securit_group


user-email-index (for authentication only)
    email, primary_key, partition_key
    user_id
    password_digest


board
    board_id, primary_key
    title
    description


post
    post_id, primary_key, partition_key
    nth, primary_key, sort_key
    board_id
    title
    content
    author_id
    create_at
    update_at


post-author_id-post_id (for finding all post authored by an user)
    author_id, primary_key, partition_key
    create_at, primary_key, sort_key
    post_id


post-board_id-create_at (for finding all post authored by an user)
    board_id, primary_key, partition_key
    create_at, primary_key, sort_key
    post_id


security_group

    security_group_id, primary_key, partition_key
    description
    action_id_list


讨论
------------------------------------------------------------------------------

这里最复杂的功能就是顶贴子了. 按照论坛的规则, 贴子的展示顺序应该按照每个贴子最后一篇回复的创建时间, 从高到低逆序排列. 有最新回复的贴子排在最前面. 比如说用户进入了 ``电脑技术`` 板块, 并访问了第2页 (假设1页展示10个贴子), 那么我们就要按照最后一篇回复的时间顺序排列贴子, 给用户展示10-20篇.


在数据表的设计上, 我们可以将 post 和 comment 放在一个表中, 默认每个贴子第 0 个 comment 是主题帖. 之后的是回复.
这样的好处是在取得贴子第一页的内容时, 不需要 Join. 但是执行只关心贴子信息的查询时, 不可避免的也要扫描很多 comment.

另一个办法是, 我们可以将 post 和 comment 放在不同的表中. 列出某个板块或者某个用户的所有贴子时, 就不用扫描 comment 了. 缺点是, 在打开贴子主题页时, 我们要访问 post 和 comment 两张表.
