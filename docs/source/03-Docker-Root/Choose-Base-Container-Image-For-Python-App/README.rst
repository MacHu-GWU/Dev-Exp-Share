.. _choose-base-container-image-for-python-app:

Choose Base Container Image For Python App
==============================================================================


Simple Tag vs Shared Tag
------------------------------------------------------------------------------
当你在 `Docker Hub <https://hub.docker.com/_/python>`_ 上搜索基础镜像的时候, 通常会看到有很多 Tags, 这些 Tags 一般被分为 "Simple Tags" 或是 "Shared Tags". 官方的解释比较冗长, 我们做一个简单的总结:

- Simple Tag: 只对一个具体的底层架构负责, 比如 Linux, Windows, X86, ARM. 不会兼容很多种架构. 通常在生产环境中, 你知道你的运行环境是什么, 选择只支持该运行环境的基础镜像即可. **这也是大多数生产环境中的选择**.
- Shared Tag: 对多个底层架构负责, 比如同时支持 Linux 和 Windows. 比如你需要构建一个纯 Python 语言, 不依赖任何 C 语言的包, 可以在 Linux 和 Windows 上运行的镜像, 你可以选择 Shared Tag 作为你的基础镜像.

官方说明:

    Some images have separated "Simple Tags" and "Shared Tags" sections under "Supported tags and respective Dockerfile links" (see the mongo image for an example).

    "Simple Tags" are instances of a "single" Linux or Windows image. It is often a manifest list that can include the same image built for other architectures; for example, mongo:4.0-xenial currently has images for amd64 and arm64v8. The Docker daemon is responsible for picking the appropriate image for the host architecture.

    "Shared Tags" are tags that always point to a manifest list which includes some combination of potentially multiple versions of Windows and Linux images across all their respective images' architectures -- in the mongo example, the 4.0 tag is a shared tag consisting of (at the time of this writing) all of 4.0-xenial, 4.0-windowsservercore-ltsc2016, 4.0-windowsservercore-1709, and 4.0-windowsservercore-1803.

    The "Simple Tags" enable docker run mongo:4.0-xenial to "do the right thing" across architectures on a single platform (Linux in the case of mongo:4.0-xenial). The "Shared Tags" enable docker run mongo:4.0 to roughly work on both Linux and as many of the various versions of Windows that are supported (such as Windows Server Core LTSC 2016, where the Docker daemon is again responsible for determining the appropriate image based on the host platform and version).

Reference:

- `What's the difference between "Shared" and "Simple" tags? <https://github.com/docker-library/faq#whats-the-difference-between-shared-and-simple-tags>`_


Full vs Slim vs Alpine vs Stretch, Buster, Jessie, Bullseye
------------------------------------------------------------------------------
当你在 `Docker Hub <https://hub.docker.com/_/python>`_ 上搜索基础镜像的时候, 你会在 Tag 中看到很多 Slim, Alpine, Stretch 等词汇. 我们来理解一下这些词汇代表的含义.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Full official image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
没有任何词汇, 只有版本号, 例如 ``X.Y.Z``.

这些镜像基于最新的稳定 Debian 操作系统, 包含了 Linux 环境中的所有工具, 例如 wget, curl, git 等等. 相当于一个完整的 Linux 虚拟机. 自然体积也是最大的. 例如 ``3.8.11`` 有 350MB.

如果你不关心最终镜像的大小, 完整镜像是最安全的选择, 也是一个保底选项.


Slim
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
包含词汇 slim, 例如 ``X.Y.Z-slim``.

这些镜像是 Full official image 的精简版, 通常只安装运行特定工具的最小包. 例如 Python ``3.8.11-slim`` 只有 35MB.

注意, 在使用这个镜像时, 一定要进行彻底的测试!


Alpine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
包含词汇 alpine, 例如 ``X.Y.Z-alpine``.

alpine 镜像基于 alpine Linux 项目, 这是一个专门为容器内部使用而构建的操作系统. 体积非常小. Alpine 基础镜像 (不包含任何编程语言的运行时, 只有 Linux 内核) 只有 5MB, 不包含任何编译所需的依赖. 如果你需要某个语言的 Alpine 镜像, 请不要用那个 5MB 的基础镜像来安装语言运行时, 而使用预装了该语言的镜像, 例如 Python ``3.8.11-alpine`` 只有 15MB.

由于它不包含编译所需的依赖, 所以一些需要编译的包, 例如比较旧的 numpy 和 pandas (旧的包不包含预先编译好的 wheel 安装文件) 是无法在 alpine 上安装的, 因为需要很多 C 依赖来编译.


bullseye / buster / stretch / jessie
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``bullseye / buster / stretch / jessie`` 是针对不同的 Debian 代号. 其中:

- bullseye: Debian 11
- buster: Debian 10
- stretch: Debian 9
- jessie: Debian 8

建议到 `Debian Release <https://www.debian.org/releases/>`_ 查看它们的支持计划, 尽量选择 Stable + LTS (Long term support) 的版本. 例如现在时 2023-06-01, 官网的状态如下. 我会选择 buster 版本, 因为他是 stable 版本, 并且处于 LTS support 中.

- The next release of Debian is codenamed bookworm — testing — release planned for 2023-06-10
- Debian 11 (bullseye) — current stable release
- Debian 10 (buster) — current oldstable release, under LTS support
- Debian 9 (stretch) — archived release, under extended LTS support
- Debian 8 (jessie) — archived release, under extended LTS support
- Debian 7 (wheezy) — obsolete stable release
- Debian 6.0 (squeeze) — obsolete stable release


Final Choice for Python App
------------------------------------------------------------------------------
- 如果你懒, 也不在乎镜像大小, 那么用 Full official image 是最安全的选择.
- 如果你在乎镜像大小, 又希望镜像稳定, 就用 slim.
- 如果你极度在乎镜像大小, 又愿意自己折腾, 就用 alpine.

- `Docker Hub Python <https://hub.docker.com/_/python>`_
- `AWS ECR Gallery Python <https://gallery.ecr.aws/docker/library/python>`_


Reference:


- `Docker Hub Python <https://hub.docker.com/_/python>`_
- `AWS ECR Gallery Python <https://gallery.ecr.aws/docker/library/python>`_
- https://aws.amazon.com/cn/blogs/china/choose-the-best-docker-image-for-your-python-application/
