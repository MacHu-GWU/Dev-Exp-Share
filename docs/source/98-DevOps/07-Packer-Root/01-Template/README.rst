Hashicorp Packer - Template
==============================================================================


Summary
------------------------------------------------------------------------------
Template 是一个定义了构建流程的脚本, 包括了用哪个镜像作为基础镜像, 构建逻辑是怎样的, 输出是什么.

在早期 Packer 用的是 JSON 来定义 build 的流程. 但是明显 JSON 无法应付复杂的情况. 在 1.7.0 之后, Packer 也启用了 HCL2, 也就是 terraform 的那个 DSL (Domain Specific Language) 作为脚本编写语言. 诚然 HCL2 不是一个通用语言, 功能有限, 但是对于 Packer 来说, 它已经足够了. 在我个人的最佳实践中, 我喜欢用 Python 中的 Jinja2 Template Language 对 HCL 语言进行封装, 这样就允许我用到 Python 中的所有功能, 基本上能做到任何事.


Blocks
------------------------------------------------------------------------------
Packer 的 Template 有很多关键的 block. 一个 block 可以理解为一个 JSON 的 field. 这些顶层的 block 下也有一些特殊的子 block. 顶层 block 中 ``build`` 最为重要, 定义了 build 的逻辑. 而其他顶层 block 都是定义了运行环境, 插件, 等 metadata. 而 ``build`` 下面又有很多子 ``block``, 详细定义了 build 的逻辑. Packer 所有的关键 block 列表如下:

- ``packer`` block type is used to configure some behaviors of Packer itself, such as the minimum required Packer version needed to apply your configuration.
- ``variable`` blocks contain configuration for variables that can either be defaulted in configuration or set by the user at runtime.
- ``locals`` blocks contain configuration for variables that can be created using HCL functions or data sources, or composited from variables created in the variables blocks.
- ``source`` blocks contain configuration for builder plugins. Once defined, sources can be used and further configured by the "build" block.
- ``data`` block defines data sources within your Packer configuration.
- ``build`` blocks contain configuration for a specific combination of builders, provisioners, and post-processors used to create a specific image artifact.
    - ``hcp_packer_registry``:
    - ``source``: 这个 source 会继承并 override 顶层的 source block 共同决定了在这个 build 中用哪个镜像作为基础镜像
    - ``provisioner``: blocks contain configuration for provisioner plugins. These blocks are nested inside of a build block. 这是 build 的重头戏, 定义了 build 的具体逻辑, 我们以后再展开讲
    - ``post-processor``: and post-processors blocks contain configuration for post-processor plugins and post-processor plugin sequences. They are also nested within build blocks.
    - ``post-processors``:

上面这个列表是按照一般编写 template 的时候的逻辑顺序排列的. 我们一般都是先定义 packer 本身的行为, 然后定义 variable 和 local variable, 然后定义 source 镜像, 最后才定义 build 的逻辑.
