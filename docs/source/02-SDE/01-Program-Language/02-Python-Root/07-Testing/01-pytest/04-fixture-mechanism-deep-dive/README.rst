.. _pytest-fixture-mechanism-deep-dive:

Pytest Fixture Mechanism Deep Dive
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

.. sectnum::


Reference:

- About Fixture: https://docs.pytest.org/en/latest/explanation/fixtures.html
- How to use Fixture: https://docs.pytest.org/en/latest/how-to/fixtures.html
- Fixture Reference: https://docs.pytest.org/en/latest/reference/fixtures.html


What Fixtures Are
------------------------------------------------------------------------------
Fixture 的中文是固定装置的意思. 简单来说, 一个测试包含:

- Arrange: 准备
- Act: 执行
- Assert: 断言 / 验证
- Clean Up: 清理

在 Python 标准库 `unittest <https://docs.python.org/3/library/unittest.html>`_ 中, setUp 和 tearDown 函数就是用来做准备和清理工作的. 这个叫做 xUnit 风格的 setup / teardown. 在 pytest 中也有 `类似的机制和语法 <https://docs.pytest.org/en/latest/how-to/xunit_setup.html>`_. 但这种风格有一个明显的弱点, 就是复用性不够强. 而 Fixture 则是更为强大, 复用性更强, 更灵活的一种机制.

- fixture 有自己的名字, 这些 fixtures 可以被不同的 函数, 类, 模块 所复用. 而 xUnit 风格的 setup teardown 函数只能在它所起作用的层级发挥作用.
- fixture 是被模块化的, fixture 可以利用其他的 fixture.
- fixture 支持更丰富的参数化, 可以被缓存.
- fixture 逻辑更容易被管理, 你可以按照顺序排列 fixtures.

.. literalinclude:: ./e01_what_fixtures_are.py
   :language: python


Fixture errors
------------------------------------------------------------------------------
如果多个 fixtures 之间按照链式彼此依赖, 那么底层的 fixture 出错会导致高层的 fixture 无法被执行, 而用到高层的测试用例也会 fail.

.. literalinclude:: ./e02_fixture_errors.py
   :language: python


"Requesting" Fixture
------------------------------------------------------------------------------
Fixture 本质上是一个函数, 这个函数只有在你需要的时候才会被使用. 当一个 Fixture 在你的测试用例函数中以参数的形式出现, 那么你的测试用例就 "Request" 了这个 Fixture.

.. literalinclude:: ./e03_requesting_fixture.py
   :language: python


Fixtures can request other fixtures
------------------------------------------------------------------------------
Fixture 本身也可以使用其他的 Fixture. 也就是你可以有一些底层的 Fixture, 然后用它们构建更高级的 Fixture, 最后在你的测试用例中使用它们.


Fixtures are reusable
------------------------------------------------------------------------------
一个 Fixture 可以被很多个测试用例所使用. 每次使用时候 Fixture 返回的对象都是新的. 举例来说:

Fixture 函数返回的对象如果是 mutable 的, 如果你使用了这个 fixture 很多次并改变了这个对象, 但每次你使用这个 fixture 的时候这个对象都是新的, 并不会出现一个测试用例中的对象被其他测试用例所改变的情况.

.. literalinclude:: ./e05_fixtures_are_reusable.py
   :language: python


A test/fixture can request more than one fixture at a time
------------------------------------------------------------------------------
一个测试用例可以使用多个 Fixture, 就像使用参数一样使用它们. 这些 Fixture 被 evaluate 的顺序和参数定义的顺序一致.


Fixtures can be requested more than once per test (return values are cached)
------------------------------------------------------------------------------
一个测试用例可以多次使用同一个 Fixture. 由于一个测试用例的输入参数和 Fixture 的函数名是一致的, 而输入参数又不可能重复, 所以这里说的是一个测试用例用到了两个 fixture, A 和 B, 其中 B 里也用到了 A. 而这时候 A 实际上只被调用了一次, 而 A 的值则是被缓存了起来.

.. literalinclude:: ./e07_fixture_can_be_requested_many_times.py
   :language: python


Auto use fixtures
------------------------------------------------------------------------------
Fixture 可以自动被执行, 而无需被 request. 只需要使用 ``@pytest.fixture(autouse=True)`` 语法即可.

.. literalinclude:: ./e08_auto_use_fixtures.py
   :language: python


Scope
------------------------------------------------------------------------------
你可以使用一个 Fixture 很多次. 但默认情况下 Fixture 的复用是函数级的, 也就是每个测试用例的函数使用 Fixture 这个 Fixture 都会被重新执行. 有时候你希望改变这个 Fixture 的复用级别, 也就是 Scope, 例如整个类, 或者整个模块中, 这个 Fixture 只被执行一次. 例如只创建一个 Database 连接.


Dynamic Scope
------------------------------------------------------------------------------
本质上就是给 Fixture decorator 一个 ``scope`` 参数 ``@pytest.fixture(scope=determine_scope)``. 这个参数是一个 callable function, 这个 function 需要进行一些运算然后返回 ``function / class / module / package / session`` 这 5 个字符串中的一个.


Setup / Teardown AKA Fixture finalization
------------------------------------------------------------------------------
Fixture 的本质就是一个函数创建一个可复用的对象或是资源 (比如数据库连接). 有时我们希望在使用后自动清除这个资源.

在 Python 中我们有 ``with`` statement. Fixture 也有类似的机制, 先 创建资源, yield 资源, 使用后清除资源.


Safe teardowns
------------------------------------------------------------------------------

