.. _trunk-base-development-workflow:

Trunk Base Development Workflow (基于主干的工作流)
==============================================================================

.. contents:: Table of Content
    :depth: 1
    :local:


参考资料:

- trunk base 官方文档: https://trunkbaseddevelopment.com/
- 分支模型与主干开发: https://www.duyidong.com/2017/10/29/trunk-base-development/
- git flow 有害论: https://cloud.tencent.com/developer/article/1100578
- 反驳 git flow 有害论: https://ruby-china.org/topics/29263


什么是 Trunk Base
------------------------------------------------------------------------------

Trunk Base 主要是解决 git flow 中由于同时存在多个 branch, 并且很多 branch 的存在时间较长, 在突发性修改需求出现时, 如果非标准化的操作很容易就导致结构混乱的的结果.

简单来说, Trunk Base 的核心就两条:

1. 除了 master, 其他 branch 都是短时间内存在的 branch, 又叫 short live branch.
2. master 在任何时候都保持可发布的状态.

为了实现这点, 我们必须要保证有:

1. 大量的单元测试 和 集成测试.
2. 自动化的 持续 构建, 测试, 部署.


什么是 Feature Toggle (如何避免发布没有完成的 Feature)
------------------------------------------------------------------------------

首先我们来了解 "为什么需要 Feature Toggle?"

在 Trunk Base 中, 多个开发者会不断的对 master 添加功能. 到了发布的时候, master 上的代码会有一些是下一个 release cycle 才用到的功能, 并且这些功能还没有完全开发完成. 如何避免发布这些没有完成的功能呢?

Feature Toggle 就是解决方案.

简单来说就是在你的代码中给每一个 Feature 都对应一个 boolean Constant Variable 作为是否使用该功能的开关. 你的单元测试可以对这个 feature 进行测试, 但是在 integration code 中调用这个 feature 的函数时, 要对这个 Constant Variable 进行判断.

Feature Toggle 也需要额外的成本进行维护. 所以需要小心的设计.

1. 你需要在代码层实现 Feature Toggle, 并维护这些 flag 常量.
2. 对这些暂时关闭的 Feature 进行 integration test 并不容易, 意味着你需要启用这个功能, 并部署到真正的环境中进行测试.
2. 在功能成熟后, 要移除 Toggle 的时候, 工作量并不少, 并且伴随着风险. 比如漏了一个 ``if THIS_FEATURE_FLAG:`` 代码没有移除.
3. 在前端代码中使用 Feature Toggle 非常不容易. 因为前端代码很难 import 这些 flag 常量. 所以 Feature Toggle 常用于后端代码.


什么是 Branch by Abstraction (如何进行大规模重构)
------------------------------------------------------------------------------

首先我们来了解 "为什么需要 Branch by Abstraction?"

不是所有的更改都可以在 ``short live branch`` 中解决的. 总是会有 ``longer to complete`` 的需求, 而这个更改无法在一个 ``release cycle``. 例如对代码进行重构. TBD 的核心价值是每一次 ``commit`` 都是一个可以上线的版本, 而重构本身对代码有很强的侵入性, 重构本身由于复杂度高, 所以很难做到小规模的增量提交而不破坏测试.

Branch by Abstraction 就是解决上述问题的方案. 该方法是通过在代码层对修改的功能进行抽象, 写一个跟你要重构的方法接口一致的 **抽象函数**, 然后用它调用 **实际的函数**. 在保持旧的代码完全不变的前提下, 实现一个新的函数或方法, 并将该函数旧的测试拷贝一份, 应用到新函数上. 最后重构完成测试无误后, 将 **抽象函数** 改为调用 **重构的新函数** 即可.

我们以 Amazon 线上商店的 item details 页面为例, 一个 item details 背后会跟多个微服务进行交互, 然后将物品信息汇总后返回给用户. 我们来试着重构这个非常复杂的 ``get_item_details()`` 方法.

.. code-block:: python

    # content of model.py

    def get_item_details(item_id):
        ... # lots of codes

.. code-block:: python

    # content of view/item_details.py
    from model import get_item_details

    def return_html(item_id):
        return get_item_details(item_id)

.. code-block:: python

    # content of test_model.py
    def test_get_item_details():
        assert get_item_details("id-001") ...
        ... # a lot of test


在重构期间, 你的代码会是这个样子的. 对同一个功能的实现会有两份, 而也会对两份实现进行相同的测试:

.. code-block:: python

    # content of model.py
    def _get_item_details_old(item_id):
        ... # lots of codes

    def _get_item_details_new(item_id):
        ... # refact the codes

    def get_item_details(item_id):
        return _get_item_details_old(item_id)

.. code-block:: python

    # content of test_model.py
    def _test_get_item_details(get_item_details_func):
        assert get_item_details_func("id-001") ...
        ... # a lot of test

    def test_get_item_details():
        _test_get_item_details(_get_item_details_old)
        _test_get_item_details(_get_item_details_new)


如何进行发布
------------------------------------------------------------------------------

对于小型项目并且发布周期非常短的项目, 例如微服务项目, 可以不使用 ``release branch``, 直接从 ``master`` 上进行发布. 对于其他的情况, 我们来谈谈如何正确使用 ``release branch`` 进行发布.

在接近 release cycle deadline 的时候, 比如 1-2 天前, 从 master 上创建一个 ``release branch`` 分支. 然后在 CI/CD 中进行全面测试后发布.
