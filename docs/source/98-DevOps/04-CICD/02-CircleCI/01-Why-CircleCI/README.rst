.. _why-circleci:

Why CircleCI (为什么使用 CircleCI)
==============================================================================

1. 无需管理服务器. 所有的计算发生在 CircleCI 数以万计的容器中. 非常容易 scale.
2. 容器的运行环境非常安全, 需要 ssh 才能访问. 在运行环境中使用敏感信息例如密码非常安全. 总体而言,
3. 使用 yml declaration language (声明式) 语言定义 jobs, 非常容易上手.
4. 非常强大的容器编排, 自由编排各个 jobs 之间的顺序, 依赖关系.
5. 每个 jobs 都在独立的 container 中运行, 支持并行, 非常容易 scale 提高速度.
6. 非常强大的 cache, 对 artifacts 高度重复利用, 提高构建速度.
7. 现代化的 configuration template 设计, 允许构建脚本的复用.
8. 强大的 API, 跟各种 VCS 深度结合, 跟各种云计算, 例如 AWS 深度结合.

CircleCI 免费账户支持 **私有仓库的测试**. 免费账户的唯一缺点就是一次同时只能并行运行一个测试. 但是能支持私有仓库, 已经很良心了.
