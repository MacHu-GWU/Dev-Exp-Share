Learn EventBridge by Doing
==============================================================================
我个人推荐的方式是用 CodeCommit repository 中的 Git 事件来触发, 然后编写 Event Pattern 对其进行过滤, 然后将其发送给 Lambda Function. 这样可以很方便地通过操作 Repo 来触发事件, 然后在 Lambda 中查看 event.

.. literalinclude:: ./lambda_function.py
   :language: python
   :linenos:

.. literalinclude:: ./test.py
   :language: python
   :linenos:
