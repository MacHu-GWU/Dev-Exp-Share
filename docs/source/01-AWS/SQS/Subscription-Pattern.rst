用 SQS 实现订阅模式
==============================================================================


案例, 网络新闻媒体
------------------------------------------------------------------------------

我们有一个网络新闻媒体, 有 娱乐, 音乐, 电影, 体育 四个板块. 在网站上我们可以浏览各个板块的新闻, 或者叫贴子吧. 同时我们可以选择订阅其中的某个板块, 于是当有新贴子发布时, 我们的邮件就会收到提醒, 包括这篇文章的链接.

简单来说, 我们的网站后台数据库中有一个叫做 post 的表, 装的是我们的贴子内容, 其中有一列是 category, 代表板块, 看起来是这个样子:

.. code-block:: python

    table.post
    |-- post_id
    |-- category_id
    |-- content
    |-- ...

然后我们有一个 API, 我们创建新的 Post 时都需要通过这个 API 创建.

那么这个订阅功能要怎么实现呢?

我们有另一个数据表叫做 Subscription, 看起来是这个样子

.. code-block:: python

    table.subscription
    |-- user_id
    |-- category_id

一个比较直接了当的做法是, 每当这个 API 被成功调用时 (新帖子被成功创建). 对数据库做一个查询:

.. code-block:: SQL

    SELECT
        T.user_id
    FROM subscription T
    WHERE T.category_id = 'Music'

然后对所有的 user_id 进行 ``send_email(user_id, post_id)``. 所以最后的代码看起来会像是这个样子:

.. code-block:: python

    response = create_post(category_id, post_content)
    post_id = response.post_id # auto generated
    subscriber_list = get_subscriber_list_by_category_id(category_id)
    for user_id in subscriber_list:
        send_email(user_id, post_id)

这样的实现有什么问题呢?

1. 首先, 创建贴子速度很快, 但是给大量用户发邮件的速度需要很长时间时间, 并且最好是并行发送. 假设有1万个用户订阅了 Music, 如果发送了几百封邮件后出现了故障, 那么后面的用户就收不到邮件了.
2. 另外, 如果你的 subscription 中的用户很多, 而且创建新 post 的速度很快, subscription 表的速度会跟不上, 并且将大量 user_id 放到内存中会导致大量 IO, 而这个 subscription 表是要用于服务与 用户订阅 和 取消订阅 功能的, 使用很频繁, 所以会影响数据库性能.
3. 如果有多个相同 category 的贴子被连续创建, 连续执行多个一样的 SQL 效率很低.

解决方案:

1. 发送 email 和 创建 post 应该是异步. 创建 post 之后, 把 category_id 给出来之后, 就可以结束了. 交给推送系统来处理.
2. 执行1万次 ``send_email(user_id, post_id)`` 的行为不能使串行, 而要是并行, 并且得尽量保证对每个用户只发送一次.
3. 用 SQL 取得所有订阅了某个频道的 user_id, 并不够快, 需要某种缓存机制, 能在任意时刻迅速的获得订阅了某个 category_id 的所有 user_id.

好了, 我们来一步步的用 AWS 来实现这个系统.

**用缓存为获取订阅了某个 category 的全部 user_id 提速**:

我们可以创建一个 Redis 缓存数据库, key 是 category_id, value 是一个 set, 里面存放着订阅的 user_id. 在 用户订阅, 和取消订阅 的 API 中, 我们除了跟 subscription 的 关系数据库交互, 还跟 缓存数据库 交互, 将 user_id 在缓存 set 中更新 / 删除.

Redis 支持有 4 Billion 个元素的集合. 而且 Redis 数据库在启动时, 可以暂时从专用只读的 replica 中, 从 subscription 表中读取初始数据. 所以我们并不需要为缓存数据做持久化.

这样, 我们可以非常快地获得, 在某个时刻, 订阅了某个 category 的全部 user_id.

**给所有的 user_id 发 email**

我们可以创建一个 SQS, FIFO Message Queue (F-Q). 每当新的 post 被成功创建之后, 把 category_id 发送到这个 F-Q. 然后触发一个 Job Scheduler Lambda.
这个 Lambda 从缓存中读取所有订阅用户的 user_id.

假设该主题有 N 个订阅用户, 我们现在要做的事情是, 生成 N 条消息, 每条消息的内容是一个用户的 email 和 post_id, 然后将这 N 条消息发送到另一个 Q 中, 每条消息自动触发一个 Email Sender Lambda, 执行发送邮件的操作.

可是, 如果 N 很大, 我们在 Lambda 的时限5分钟内, 我们不一定能全部发送出去全部 N 条消息, 那又该怎么办呢?

首先, 假设我们用1秒发送一条 SQS 消息, 这个时间足够确保一条消息发送完成了. 那么5分钟我们能确保发出去300条消息. 所以我们可以让 Job Scheduler Lambda 将全部的 N 消息按照每 300 条一打包, 发送给另一个 SQS, 然后这个 SQS 将所有的消息分发给 Email Sender Lambda 所连接的 SQS 即可. 这样, 我们只要在5分钟内发送 N / 300 条即可.


**一些扩展思考**:

在本案例中, 我们要给用户发送 Email. 而批量广播发送 Email 这件事有很多专业的服务可以做的更好, 比如 AWS SES, Send Grid, Mail Chimp. 但是我们主要是为了实现 **订阅**, **推送** 这一抽象概念, 就不用深究用 SQS + Lambda 群发 Email 的合理性了.

在实际的新闻类 App 中是怎么做的呢? 用户登录网站或移动App后, 会在App里的通知中心看到没有被读过的提醒, 用户可以自己选择哪些提醒被点开, 哪些不被点开. 而同一时间内用户未读的提醒是不会太多的. 所以在这种情况下, 只要用一个分布式的数据库, Key 是 user_id, Value 是推送消息的 Metadata, 比如 post_id. 而实际占用空间较大的 Content 则由用户手动点开提醒后, 再动态读取即可.

在这个案例中, 我们通过使用了两个 SQS 进行分流, 使得每个 Lambda 处理的事情尽量少. 其实我们总共只要发送 N 条消息, 但我们实际发送了 N + N / 300 条. 如果我们分流的层级越多, 那么中间牵涉到的 SQS 也就越多, 多个系统耦合时故障率也就越大. 至于怎么实现一个完全横向扩展, 而不是纵向层级扩展的系统, 就留给你自己思考了.

**我们还能不能做的更好?**

在发送邮件时, 我们是基于用户的 user_id, 然后到数据库中查找到 email, name 等信息, 然后根据模板动态创建 Email.

**该架构所能支持的并发上限**

- FIFO SQS 接受的速度上限是 300条/秒
- Lambda 的并发上限是同时 1000次
- 发送一条 Q 要 0.1 秒, 也就是说 5 分钟我们可以发送 300 / 0.1 = 3000 条消息. 为了保证 5分钟能做完所有时, 我们可以让每条消息中包含 500 个 user_id
- 假设发送一个包含 500 个 user_id 的消息包的时间是 1 秒, 那么我们 5 分钟可以发送 300 个消息包, 也就是一共 150,000 个 user_id. 所以如果每个频道的 subscriber 的数量超过 150,000, 那么我们就要考虑这个系统存在的必要了.
