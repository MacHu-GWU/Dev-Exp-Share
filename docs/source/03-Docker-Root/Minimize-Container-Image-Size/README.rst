.. _minimize-container-image-size:

Minimize Container Image Size
==============================================================================
Keywords: Minimize, Reduce, Decrease, Docker, Container, Image, Size


为什么要减小镜像大小
------------------------------------------------------------------------------
原因如下:

- 你在部署的时候拉取的镜像越小, 部署的速度也就越快.
- 一个容器镜像应该是为了运行一个应用程序所需的所有环境和依赖的 snapshot. 所有不是 "运行" (注意是运行, 而不是 "构建") 所需的东西都可以被摒弃.


减少镜像体积的方法汇总
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 使用合适的小体积的基础镜像
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这个很好理解, 基础镜像决定了你的镜像的最小体积.

至于如何选择基础镜像, 可以参考 :ref:`choose-base-container-image-for-python-app`.


2. 减少 docker 镜像的 layer 的数量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一个 Image 中包含了所有在构建时所生成的 Layer. 你的 Dockerfile 中的 ``COPY``, ``ADD``, ``RUN`` 命令都会增加 Layer. Layer 可以理解为中间状态, 但是很多时候这些中间状态是不需要的. 例如你有一个三步的构建需求:

1. 下载依赖的安装文件
2. 安装依赖
3. 移除依赖

如果你为每一个步骤写一个 RUN, 那么每一个步骤的中间状态都会被记录在 Layer 中. 很明显 #1 中的安装文件我们最后是不需要的, 那么你就可以用 ``&&`` 连接两个命令, 从而减少一个 Layer. 你还可以用 ``\`` 来换行, 从而增加可读性. 例如:

.. code-block:: Dockerfile

    RUN echo 1 # this is dummy command
    RUN echo 2 # this is dummy command
    RUN echo 3 # this is dummy command

可以改写为:

.. code-block:: Dockerfile

    RUN echo 1 && \
        echo 2 && \
        echo 3

基本上合并 RUN 步骤是有益无害的. 如果这些命令非常复杂难以在 Dockerfile 中编写, 而你的基础镜像又是有 Python 的, 那么你可以用 ``run.py`` + ``subprocess`` 模块来实现你的自动化脚本, 然后将其拷贝进去执行. 看起来像是这个样子:

.. code-block:: Dockerfile

    COPY ./run.py ./
    RUN python run.py


3. 镜像只包含程序运行所需的最小的资源
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**首先是排除不必要的资源**

很多人喜欢把 Git 项目目录全部拷贝进去, 这样做经常会将一些缓存, 临时文件也拷贝进去了, (Python 项目中还可能会把硕大的虚拟环境拷贝进去). 这些都不是必要的. 你可以用 `.dockerignore <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#exclude-with-dockerignore>`_ 来排除这些文件.

**按照程序语言的运行特性做对应的资源裁剪**

例如我们构建时如果需要安装一些 Linux 工具, 例如 slim 版本中缺少 curl 工具. 而包管理工具会产生很多临时缓存, 你可以在安装完之后对其进行清理, 例如:

.. code-block:: Dockerfile

    # /var/lib/apt/lists/* 是 apt 的临时安装目录, 安装完之后可以删除
    # 在不同的镜像中这个可能不一样, 请自行确认
    RUN apt update -y && apt install -y curl && rm -rf /var/lib/apt/lists/*

再例如对于编译型语言 golang, 因为最终会生成一个二进制的可执行程序, 所以你的最终环境中是不需要编译所需的运行环境的, 包括 go 运行时本身. 那么你就可以用多阶段构建来实现. 这个我们在下一节详细说.


4. 使用多阶段构建技术
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`multi-stage builds <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#use-multi-stage-builds>`_ 是我们构建过程中相对来将复杂一段的技术, 但是也异常的实用. 它的核心思想是: 将 Docker 镜像的构建分为多个阶段, 下一个阶段依赖上一个阶段的输出, 将上一个阶段的输出作为输入来排除掉上个阶段构建过程中无法排除的废弃文件. 由于下一个阶段的构建可以视为是一个基于另一个基础镜像的全新构建, 第一个阶段中的所有中间状态和 Layer 都不会被保留, 从而达到减小镜像体积的目的.

这里我们用 Go 编译语言来举例. 我们有一堆 Go 源码, 需要打包成镜像. 传统做法是使用 ``FROM golang:1.16-alpine`` 构建, 编译, 结束. 而使用多阶段构建的做法是:

1. 用带有 golang 运行时的基础镜像编译源码为二进制可执行文件, 并输出.
2. 用 scratch 作为基础镜像, 将上一步的二进制可执行文件拷贝进去, 并设置为入口命令.

假设带有 golang 的镜像是 50MB, 你的源码是 100KB, 编译好的程序是 1MB, 而 scratch 可能只有 1KB. 用传统方法构建的镜像大小至少是 50 + 1 + 构建时生成的中间产物 MB. 而用多阶段构建生成的镜像只有 1KB + 1MB. 这是一个非常大的差别.

.. code-block:: Dockerfile

    # syntax=docker/dockerfile:1
    FROM golang:1.16-alpine AS build

    # Install tools required for project
    # Run `docker build --no-cache .` to update dependencies
    RUN apk add --no-cache git
    RUN go get github.com/golang/dep/cmd/dep

    # List project dependencies with Gopkg.toml and Gopkg.lock
    # These layers are only re-built when Gopkg files are updated
    COPY Gopkg.lock Gopkg.toml /go/src/project/
    WORKDIR /go/src/project/
    # Install library dependencies
    RUN dep ensure -vendor-only

    # Copy the entire project and build it
    # This layer is rebuilt when a file changes in the project directory
    COPY . /go/src/project/
    RUN go build -o /bin/project

    # This results in a single layer image
    FROM scratch
    COPY --from=build /bin/project /bin/project
    ENTRYPOINT ["/bin/project"]
    CMD ["--help"]

而对于解释性的语言例如 Python, 这样做的优势就不大了. 因为你最终运行还是要带上 Python 运行时, 而且你的代码没有编译的需要, 你直接拷贝进去, 把依赖安装好, 清除掉安装缓存即可. 但是如果你有一些需要编译的依赖, 例如 Numpy, Pandas, 这些包在 Alpine 上安装不了, 那么你就可以用多阶段构建, 先用普通 Full official 将其安装好, 然后将 site-packages 文件夹作为输入拷贝给下一个阶段, 并在下一阶段中使用 Alpine 作为你的最终 Image.


Reference
------------------------------------------------------------------------------
- Docker 镜像瘦身技巧: https://juejin.cn/post/7074981052233711647