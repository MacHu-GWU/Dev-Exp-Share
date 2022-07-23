.. _consistent-behavior-in-cicd:

Consistent Behavior in CI/CD
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Summary
------------------------------------------------------------------------------
在 CI/CD 中, 我们的代码需要经过几个环境的测试, 才能最终到达生产环境. 这几个环境包括了:

1. 本地开发电脑 local
2. 本地单元测试, 确保在将代码 commit 到 git 之前代码没问题
3. CI 的单元测试, 在 CI 里再跑一边, 自动运行单元测试, 及早发现错误
4. 部署真正的 App 到 dev 环境, 以供后续开发使用.
5. 用 dev 环境的代码做集成测试.
6. 在 CI 里 build artifacts.
7. 将 artifacts 部署到 qa 环境中, 继续运行单元测试和集成测试.
8. 最终验证没问题后将 artifacts 部署到 prod 环境中.

这些环境的运行时经常会各不相同, 有的是本地机器, 有的是虚拟机, 有的是容器. 而这里最大的挑战就是 **如何让一套核心业务代码逻辑能在各种不同的环境下都能正常运行**?
