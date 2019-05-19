.. _amazon_state_language:

Amazon State Language
==============================================================================
ASL是一种用json来定义Step Function的语言. 其核心概念是 ``State`` 和 ``Task``.

- State概念: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html
- Task概念: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-tasks.html

ASL的详细文档可以参考: https://states-language.net/spec.html

.. _asl_state:

State
------------------------------------------------------------------------------

State是有限状态机中的状态, 一个有限状态机可能有若干个状态. 而至少要有一个Start和Stop状态. 而State按照相关的Action, 又有以下几种类别(参考自 https://states-language.net/spec.html#toc):

- Pass State
- Task State
- Choice State
- Wait State
- Succeed State
- Fail State
- Parallel State


.. _asl_task:

Task
------------------------------------------------------------------------------

Task是一种特殊的State, 是所有State中真正能执行某种动作的.



Finite State Machine(有限状态机)
------------------------------------------------------------------------------

FSM是表示有限个状态以及在这些状态之间的转移和动作等行为的数学模型, 在有限状态机中, 要尽量避免循环. 以我的个人理解有限状态机就像是转移过程有动作的马尔科夫链.

介绍有限状态机的文章:

- Wiki有限状态机: https://zh.wikipedia.org/wiki/%E6%9C%89%E9%99%90%E7%8A%B6%E6%80%81%E6%9C%BA
- 深入理解有限状态机: https://www.jianshu.com/p/5eb45c64f3e3
