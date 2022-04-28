Loguru 是一个日志库, 实现简单, 功能强大, 依赖很少.


Loguru 的设计
------------------------------------------------------------------------------
1. Logger, 日志打印机, 所有的日志都是从 logger 发出去的.
2. Handler, 日志处理者, 决定了日志发到哪里去, 格式是什么, 要不要做修改, 有没有过滤器. Handler 是由 ``Logger.add`` 方法创建的, 创建后会返回一个 handler_id, 你可以用 ``Logger.remove(handler_id)`` 将其删除. 默认的 handler 是发送到 stderr 的, 你可以用 ``Logger.remove()`` 来删除之. 如果不给参数, remove 会删除最后一个 handler.
3. Record, 就是一个 dict 字典, 里面不仅包含了 message, 还包含了 logger 本身的 metadata, 还有很多其他信息. 每次发送一个 log 的时候其实会生成一个 record, record 会经过 handler 的处理之后才发送.
4. Sink, 是 handler 的子概念, 一个 handler 最关键的就是 sink, 这个 log 要被发到哪里? 是 stderr, stdout, 还是文件?
5. Filter, 是 handler 的子概念, 每个 Record 会经过 handler 中的 filter 过滤以决定是否要发出去.
6. Bind, 生成一个新的 Logger, 并给其绑定一些 metadata.


有几点特别注意事项
------------------------------------------------------------------------------
1. Handler 的注册是全局有效的, 并不是说 handler 就跟 logger 互相绑定了.