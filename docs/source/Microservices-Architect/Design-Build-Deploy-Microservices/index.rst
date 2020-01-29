Design Build Deploy Microservices
==============================================================================

.. contents::
    :depth:
    :local:

参考资料:

- 设计, 构建, 部署 微服务系列文章: https://www.jianshu.com/p/8d2cfa1fa633
- Design, Build, Deploy Microservices: https://www.nginx.com/blog/introduction-to-microservices/


微服务介绍, 好处, 坏处, 常见的坑
------------------------------------------------------------------------------

- Monolithic Architect: 单体式架构
- Micro Services Architect: 微服务架构

Monolithic Architect Challenges:

- High Dependencies
- Language Framework
- Hero Deployment
- Scaling

Micro Service Advantage:

- Pick your own language
- Manage your own DevOps pipeline
- Less Risk in Challenge
- Independent Scaling, Easy to Scale
- Easy to Reuse, orchestrate services to build a business logic

Micro Serivce Disadvantage:

- More complexity for service Integration. All Caller Failure, Overloading, Runtime Error has to be properly handled.
- Higher latency, low performance, chained services introduces higher latency


使用 API Gateway
------------------------------------------------------------------------------

**没有 API Gateway 会怎么样**?

在微服务架构下, 在我做过的一个政府部门的 CMS Portal 项目中, 有一个页面要展示用户的很多信息. 比如 身份信息, 医疗记录, 财政记录 等等. 这些不同的记录对应着很多个 service. 那么在一个 ``GET /user-details/<user-id>`` 的请求中, 在客户端写多个 service 的请求是不明智的. 因为这些请求可能会有的失败, 有的成功, 而且每个协议可能还不一致, 有的是 RPC, 有的是 AMQP. **这样会导致你的客户端程序非常复杂且难以维护**. 并且在当我们对服务进行重构, 拆分或合并微服务的时候, **保持服务端代码和客户端代码的同时重构会异常困难**. 另外从安全和效率的角度, 由于 每个 Service 的协议并不相同, 有的适合用 https 走公网, 有的适合在私网上运行. 由客户端从公网直接调用私网的 API 会导致在客户端会驻留私网 IP 之类的信息, 一不安全, 二通信慢.

**API Gateway 是什么?**

**API Gateway 的职责是为每个客户端提供定制化的 API**, 为客户端提供粗粒度的API. 而这些后面复杂的调用多个 service 的整合工作, 则由 API Gateway 实现. 而 API Gateway 通常部署在离微服务近的地方, 调用微服务 API 的速度比直接从客户端调用要高.

**使用 API Gateway 的好处和坏处?**

好处:

- 客户端复杂度低, 单个 API 的测试比较容易, 开发效率高.
- API Gateway 和内部服务通信效率高, 速度快, 且安全.

坏处:

- API Gateway 本身是一个高可用的组件, 需要被开发, 部署, 管理. 服务端开发者开发后要相应的更新 API Gateway (幸好有 AWS API Gateway 把这些都解决了)

**API Gateway 中的核心设计**

1. 性能与扩展性 (performance and scalability): 使用异步非阻塞的方式实现.
2. 使用响应式编程模型 (Reactive programming model): 不要使用异步回调的模型 (Callback) 这样会导致你的代码纠缠不清. 各个 service 的调用可以是并行的也可以是有依赖的.
3. 服务调用 (Service Invocation): 可以是 同步调用 或是 异步调用 又或是 消息中间件 模式. API Gateway 需要支持这些通信机制.
4. 服务发现 (Service Discovery): API Gateway 需要知道每一个 Service 的端口和地址, 在 microservice 架构中你需要有一个高可用强一致的系统能在 每个 service scale up and down 的时候发现这些.
5. 处理局部故障 (Handling Partial Failures): 一个 API Call 可能涉及到多个 Service, 出错的原因可能是 请求格式不正确, 服务处理时出错, 服务处理超时, 服务不可用. 出错的服务可能是重要服务或是不重要的服务 (例如个性化推荐系统的结果可以不成功, 不成功时就推荐全局的推荐结果即可). 此时要妥善处理故障.


微服务架构中的进程间通信
------------------------------------------------------------------------------

**交互风格 (Interaction Styles)**:

总共有下面几种:

- 一对一, 同步 (请求/响应)
- 一对一, 异步 (通知)
- 一对一, 异步 (请求/异步响应)

- 一对多, 同步 (逻辑上不成立, 没有这种模式, 因为多个响应端不可能同时响应, 那么该通信整体来说就是异步的)
- 一对多, 异步 (发布/订阅)
- 一对多, 异步 (发布/异步响应)

术语解释:

- 一对一: 每个客户端请求只会被一个服务实例处理.
- 一对多: 每个请求将会被多个服务实例处理.
- 同步: 客户端期望来自服务端的及时响应, 甚至可能阻塞并等待.
- 异步: 客户端等待响应时不会阻塞, 对异步来讲, 及时响应并不是必须的.

一对一的交互方式:

- 请求/响应模式: 客户端向服务端发送请求并等待响应, 并期望服务端可以及时的返回响应. 在一个基于线程的应用中, 发出请求的线程可能在等待时阻塞线程的执行.
- 通知 (也就是单向请求): 客户端往服务端发送请求, 但并不等待响应返回.
- 请求/异步响应: 客户端往一个异步返回响应的服务发送请求. 客户端等待式并不会阻塞线程, 因为设计时就假设请求不会立即返回 (js回调).

一对多的交互方式:

- 发布/订阅模式: 客户端发布一个通知消息, 消息将会被0或多个感兴趣的服务消费.
- 发布/异步响应: 客户端发布一个请求消息, 并在一定时间内等待消费消息的服务响应.

**故障处理 (Error Handling)**:

- **网络超时 (Network timeouts)**: 等待响应时不要一直阻塞, 而是使用超时, 超时能够保证资源不会一直被占用
- **限制未完成请求的数量 (Limiting the number of outstanding requests)**: 针对一个请求某服务的客户端, 需要设置其未处理请求数量的上限, 一旦超过限制就不再处理任何请求, 这样就做到快速失败.
- **断路器模式 (Circuit breaker pattern)**: 跟踪成功和失败请求的数量, 如果比率超过了设置的阀值, 打开断路器使得后续请求快速失败. 如果大量请求失败, 就建议服务为不可以状态并决绝处理新请求, 过一段时间之后, 客户端可以再次重试, 一旦成功, 关闭断路器.
- **提供fallback机制 (Provide fallbacks)**: 请求失败时提供fallback, 比如返回缓存值或者为失败的推荐服务返回默认空集合作为默认值.

