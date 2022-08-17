.. _polars-root:

polars Root
==============================================================================
`polars <https://www.pola.rs/>`_ 是一个速度非常快的 DataFrame 的库. 它经常被拿来与 pandas 进行比较, 因为它们有着相似的语法. 但其实 polars 的目标并不是用来替代 pandas, 它有自己的使命, 只不过提供一套类似 pandas 的语法能够降低开发者的学习成本.

要理解 polars 的独特之处, 你必须要了解 `arrow <https://arrow.apache.org/>`_.

**arrow** 是 Apache 基金会的一个开源项目, 它本身与编程语言无关. arrow 是一套基于列向量计算的一套紧凑内存模型, 这种内存模型特别适合对大量数据利用多 CPU 和 GPU 并行计算. arrow 的这套技术对于主流的编程语言都有对应实现. 其中 pyarrow (Python 实现, 基于 C, API 用 Python 封装, 调用底层的 C) 本身就有和 pandas 所类似的语法实现, 但是很多 pandas 的 API 并不支持, 因为它本质是一个向量计算的库. 现在我们可以来了解 polars 了.

polars 是基于 arrow 开发的一套 DataFrame 系统, 既有 arrow 的高性能, 也有 pandas 的那非常友好的 API. polars 所依赖的 arrow 不是 apache 官方的 `arrow-rs <https://github.com/apache/arrow-rs>`_, 而是 arrow 的核心开发者之一的 Jorge Leitao 的开源项目 `arrow2 <https://github.com/jorgecarleitao/arrow2>`_. arrow2 相比官方的实现有着 更加安全, 可以安全的读取来历不明的 parquet 传文件, 以及致力于 transmute-free (零转换), 避免在读写拷贝数据的时候产生实际的内存拷贝. polars 依赖于底层的 arrow2, 并对其进行了封装以提供用户友好的 API. polars 本身是用 rust 写的, 由于 rust 是可以编译成一个二进制文件从而让用户无需安装 rust 即可使用, 所以 polars Python 本质上是自带了一个二进制的 rust 编译文件, 用户的 Python API 调用的都是底层的 rust 库.
