
Restrict CPU, Memory, GPU usage of Docker Container (限制容器所使用的系统资源)
==============================================================================

.. contents::
    :depth: 1
    :local:


限制容器可用的 CPU 算力
------------------------------------------------------------------------------

**指定容器最多使用的 CPU 算力**:

关键命令 ``docker run --cpus=1``, 1 表示总算力为相当于 1 个 CPU 100% 为该容器工作, 2 表示相当于 2 个... 这里说相当于是因为现在的计算机大多是多核系统, 而容器并不会完全占有其中的几个 CPU, 而是平均分配到所有的 CPU 上. 例如 你如果有 4 块 CPU, 而你的设置为 1, 那么每个 CPU 会提供 25% 的算力给该容器.

**指定固定的 CPU**:

关键命令, 指定运行容器的 CPU 编号为 1: ``docker run --cpuset-cpus="1"``.

通过 --cpus 选项我们无法让容器始终在一个或某几个 CPU 上运行, 但是通过 --cpuset-cpus 选项却可以做到! 这是非常有意义的, 因为现在的多核系统中每个核心都有自己的缓存, 如果频繁的调度进程在不同的核心上执行势必会带来缓存失效等开销.

**设置使用 CPU 的权重**:

关键命令, ``docker run --cpuset-cpus="1" --cpu-shares=512``

当 CPU 资源充足时, 设置 CPU 的权重是没有意义的. 只有在容器争用 CPU 资源的情况下, CPU 的权重才能让不同的容器分到不同的 CPU 用量. --cpu-shares 选项用来设置 CPU 权重, 它的默认值为 1024. 我们可以把它设置为 2 表示很低的权重, 但是设置为 0 表示使用默认值 1024.

举例来说, 我们启动了两个容器, 都指定使用 CPU1. 这里的权重分别为 512 和 256, 则两个容器对 CPU 的占用率分别为 66% 和 33%.

.. code-block:: bash

    $ ``docker run --cpuset-cpus="1" --cpu-shares=512``
    $ ``docker run --cpuset-cpus="1" --cpu-shares=256``


限制容器所能使用的内存
------------------------------------------------------------------------------

限制容器不能过多的使用主机的内存是非常重要的. 对于 linux 主机来说, 一旦内核检测到没有足够的内存可以分配, 就会扔出 OOME(Out Of Memmory Exception), 并开始杀死一些进程用于释放内存空间. 糟糕的是任何进程都可能成为内核猎杀的对象, 包括 docker daemon 和其它一些重要的程序. 更危险的是如果某个支持系统运行的重要进程被干掉了, 整个系统也就宕掉了！这里我们考虑一个比较常见的场景, 大量的容器把主机的内存消耗殆尽, OOME 被触发后系统内核立即开始杀进程释放内存. 如果内核杀死的第一个进程就是 docker daemon 会怎么样？结果是所有的容器都不工作了, 这是不能接受的！

针对这个问题, docker 尝试通过调整 docker daemon 的 OOM 优先级来进行缓解. 内核在选择要杀死的进程时会对所有的进程打分, 直接杀死得分最高的进程, 接着是下一个. 当 docker daemon 的 OOM 优先级被降低后(注意容器进程的 OOM 优先级并没有被调整), docker daemon 进程的得分不仅会低于容器进程的得分, 还会低于其它一些进程的得分. 这样 docker daemon 进程就安全多了. 

我们可以通过下面的脚本直观的看一下当前系统中所有进程的得分情况:

.. code-block:: bash

    #!/bin/bash
    for proc in $(find /proc -maxdepth 1 -regex '/proc/[0-9]+'); do
        printf "%2d %5d %s\n" \
            "$(cat $proc/oom_score)" \
            "$(basename $proc)" \
            "$(cat $proc/cmdline | tr '\0' ' ' | head -c 50)"
    done 2>/dev/null | sort -nr | head -n 40

此脚本输出得分最高的 40 个进程, 并进行了排序:

第一列显示进程的得分, mysqld 排到的第一名. 显示为 node server.js 的都是容器进程, 排名普遍比较靠前. 红框中的是 docker daemon 进程, 非常的靠后, 都排到了 sshd 的后面. 

有了上面的机制后是否就可以高枕无忧了呢！不是的, docker 的官方文档中一直强调这只是一种缓解的方案, 并且为我们提供了一些降低风险的建议: 

- 通过测试掌握应用对内存的需求
- 保证运行容器的主机有充足的内存
- 限制容器可以使用的内存
- 为主机配置 swap
- 好了, 啰嗦了这么多, 其实就是说: 通过限制容器使用的内存上限, 可以降低主机内存耗尽时带来的各种风险. 

**限制内存使用上限**

.. code-block:: bash

    $ docker run -m 300M --memory-swap -1

上面的 docker run 命令中通过 -m 选项限制容器使用的内存上限为 300M. 同时设置 memory-swap 值为 -1, 它表示容器程序使用内存的受限, 而可以使用的 swap 空间使用不受限制(宿主机有多少 swap 容器就可以使用多少). 

**限制可用的 swap 大小**

强调一下 --memory-swap 是必须要与 --memory 一起使用的. 

正常情况下,  --memory-swap 的值包含容器可用内存和可用 swap. 所以 --memory="300m" --memory-swap="1g" 的含义为:

容器可以使用 300M 的物理内存, 并且可以使用 700M(1G -300M) 的 swap. --memory-swap 居然是容器可以使用的物理内存和可以使用的 swap 之和！

把 --memory-swap 设置为 0 和不设置是一样的, 此时如果设置了 --memory, 容器可以使用的 swap 大小为 --memory 值的两倍. 

如果 --memory-swap 的值和 --memory 相同, 则容器不能使用 swap. 下面的 demo 演示了在没有 swap 可用的情况下向系统申请大量内存的场景: 

.. code-block:: bash

    $ docker run -it --rm -m 300M --memory-swap=300M

demo 中容器的物理内存被限制在 300M, 但是进程却希望申请到 500M 的物理内存. 在没有 swap 可用的情况下, 进程直接被 OOM kill 了. 如果有足够的 swap, 程序至少还可以正常的运行. 


Reference
------------------------------------------------------------------------------

- Runtime Options with Memory, CPUs, GPUs: https://docs.docker.com/config/containers/resource_constraints/
- Docker 限制可用的 CPU 个数:  https://www.cnblogs.com/sparkdev/p/8052522.html
- Docker 限制容器可用的内存: https://www.cnblogs.com/sparkdev/p/8032330.html
