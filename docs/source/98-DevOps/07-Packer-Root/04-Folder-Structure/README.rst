Hashicorp Packer - Folder Structure
==============================================================================


Summary
------------------------------------------------------------------------------
Packer 和 terraform 类似, 你的项目需要 follow 特定的目录结构, 文件名也要遵循一定的规律, 这样 Packer 才能找到对应需要的文件.

注: 本文以 HCL2 template 为准, 我们不再学习 JSON template 了.

简单来说, 有两种扩展名文件:

1. ``*.pkr.hcl``, 这个是 packer template 的定义文件. Packer 运行的时候如果指定的目标是一个文件夹, 那么 Packer 会自动将这个文件夹下所有的 ``*.pkr.hcl`` 文件 merge 到一起. 这意味着你可以把 variables, source, build 等 block 分到很多个文件中去.
2. ``*.pkrvars.hcl``, 这个是 hardcoded 的 variable 是的 key value 对. 你可以用 ``packer build -var-file="variables.pkrvars.hcl .`` 来指定用这个文件中的内容作为你的 variables 的值. 而如果你当前目录下有 ``*.auto.pkrvars.hcl`` 文件, 这些文件的内容会自动被 load 进去, 而无需手动指定 ``-var-file``.