.. _aws-code-artifact-basic:

CodeArtifact Basic
==============================================================================
Keywords: AWS CodeArtifact, Code Artifact

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Code Repository Server
------------------------------------------------------------------------------
这里我们以 Python 为例来解释, 对于其他编程语言, 原理是一样的.

**什么是 Code Repository Server**

Python 开发者肯定用过 ``pip install requests`` 这样的命令或者 ``pip install -r requirements.txt`` 这样批量安装多个依赖. pip 的原理是 Python 官方维护了一个 public 的 https://PyPI.org 服务器. 开源库的开发者会将包发布在 PyPI 上, 然后 pip 默认也会去 PyPI 上去找包. 这个 PyPI.org 本质上就是一个 Server, 支持了一些 Python 社区所规定的 protocol. 类似 PyPI.org 的系统就叫做 Code Repository Server.

**为什么需要 Code Repository Server**

虽然 pip 支持很多种的安装方式, 例如从文件夹安装 (只要文件夹里的文件有 setup.py 并符合规范), 或是从 git 安装. 对于企业用户而言, 很多库都是不能公开的. 而如果将这些包 host 在 git 上或是任何文件系统上, 会带来几个问题:

1. ``pip install requests`` 的时候如果不显式告知具体版本, pip 不知道怎么去 git 上查找所有的版本信息.
2. 你必须用 ``pip install https://github.com/corp/my_library.git`` 这样的命令来安装, 这会导致你的所有 requirements.txt 文件中的定义非常难以维护.
3. 你的私有包可能依赖于其他的私有包. 这些依赖关系是在 setup.py 中维护的, 一旦发布就无法修改了. 你没法在 setup.py 中指定 ``install_requirements=["https://github.com/corp/my_library.git",]`` 这样的依赖.

所以你需要一个私有的 PyPI, 然后把包放在私有 PyPI 上, 然后直接对 pip 进行一下 configure 使其能访问私有的 PyPI, 然后就跟平时一样用 ``pip`` 命令安装即可.


What is CodeArtifact
------------------------------------------------------------------------------
CodeArtifact 是 AWS 的一个服务, 只需要简单的几下点击, 就可以获得一个私有的 Code Repository Server. 目前 CodeArtifact 支持:

- Python with PyPI
- Node.js with NPM (NPM 和 PyPI 类似, 不过是服务于 Node.js 的, 定义的接口有所不同)
- Java with Maven
- .Net with Nuget


CodeArtifact Concepts
------------------------------------------------------------------------------
- Repository: 一个 Repository 就是一个 Code Repository Server 的服务器, 一个 CodeArtifact Repository 等同一个 PyPI. 你用 pip 之前先要用 AWS CLI 鉴权, 这会对 PyPI 的 config 文件自动进行配置, 使其能跟你的 CodeArtifact Repository 进行通信, 并优先使用之.
- Upstream repository: 如果你为你的 pip 客户端配置了 PyPI 使其能优先使用你的 CodeArtifact Repository. 如果 pip 找不到指定的包, 则会到 upstream repository, 也就是默认的 public PyPI 上去找. 这样就可以用 pip 命令同时安装私有包和开源包了. **这本质上就是一个层级的搜索树, Public PyPI 是 root, 你私有的 Repo 是 leaf, pip 会从 leaf 搜索起, 如果搜索不到则会到上一层的 Repo 中搜索**
- Domain: 一个 Domain 会将多个 Repository 聚集到一起, 一个 Domain 下可以有多个 PyPI, 多个 NPM, 多个 Maven, 多个 Nuget 等.
- Package: 一个具体的包
- Package Version: 一个包的具体版本
- Asset: 一个 Package Version 下可能有多个 asset, 比如为 Windows X86, Mac Intel, Mac Arm, Linux 都维护一个 build.
