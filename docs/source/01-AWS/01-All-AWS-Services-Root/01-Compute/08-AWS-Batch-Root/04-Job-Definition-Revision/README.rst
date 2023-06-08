AWS Batch Job Definition Revision
==============================================================================


如何能判断你要创建的 Revision 和之前的有没有区别?
------------------------------------------------------------------------------
我们在自动化运维的过程中, 会用 ``register_job_definition`` API 创建一个新的 Revision. 但是如果是和之前的 Revision 完全一样的话, 我们就不需要创建了. 但是如何快速判断两个 Revision 是不是一样呢? 显然, 你拿你要注册的 Revision 和上一个详细比较是可以的, 但是你的输入是一个 JSON, 而返回的数据结构可和你输入的不一样, 非常难以实现. 我的做法是每次创建新的 Revision 的时候, 将 API 的参数变成 Python 字典 kwargs 的形式, 并序列化成 JSON (要对 Key 进行排序哦), 然后计算 SHA256 值, 作为这个 Revision 的唯一标识, 并将其保存在 Tag ``tech:revision_sha256`` (注意, 计算的时候这个 Tag 参数本身不参与计算). 这样, 下次再注册新的时你只要用 ``describe_job_definitions`` 获得之前的所有版本的 Tag, 然后快速判断一下即可. (根据我的经验, 很少有能将版本号干到 1000 以上的, 性能是有保证的). 你就可以快速判断心得 Revision 在以前是否出现过了.

- `register_job_definition <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/register_job_definition.html>`_
- `describe_job_definitions <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_job_definitions.html>`_
