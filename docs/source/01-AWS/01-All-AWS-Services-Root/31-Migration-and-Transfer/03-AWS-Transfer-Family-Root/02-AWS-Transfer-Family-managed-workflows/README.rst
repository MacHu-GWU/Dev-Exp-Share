AWS Transfer Family managed workflows
==============================================================================


Overview
------------------------------------------------------------------------------
当你将文件上传到文件服务器后, 对其采取一系列自动化操作是很常见的需求. 例如将其自动拷贝到多个需要的人的文件夹下. AWS 原生存储 S3 支持 event-driven 的 Lambda 触发器. 但对于文件服务器内, 你自己创建一个 event-driven 的触发器可不是一件容易得事情. AWS Transfer Family Workflow 相当于是吧 event-driven + Lambda 这一套东西搬到了文件服务器上. 让你无需设置 event, 也无需编写 Lambda, 就能实现常见的文件上传后的自动化操作. 当然对于不常见的, 复杂的, 自定义的操作, 你还可以自己编写 Lambda 来实现, 而将 event trigger 交给 AWS 来管理.
