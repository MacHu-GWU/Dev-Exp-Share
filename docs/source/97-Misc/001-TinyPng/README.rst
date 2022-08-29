TinyPng
==============================================================================
Keywords: Image compression, 图像压缩, Tiny PNG, TinyPNG, PNG Quant, pngquant

很多时候我们希望服务器上的图像文件能小一点以节约互联网传输资源. 或者有时候我们要把图片存在 Git 里.

TinyPNG (https://tinypng.com/) 是一个免费的网站能让你用它们的算法压缩你的图片. 虽然会牺牲一点质量但是人眼几乎看不出来. 当然你的图片里如果有敏感数据显然你自己要注意, 以及它有一次性上传数量的限制.

PNG Quant (https://pngquant.org/) 是一个用 C 写的 PNG 图像压缩的命令行工具, 其算法和 TinyPNG 用的 8 bit 位图压缩算法是一样的. 然后你自己用 Python 写一个简单的 wrapper 就可以了.

PNG Quant 的详细用法如下:

如果你是 Mac 系统:

1. 在官网 https://pngquant.org/ 下载 Binary for macOS 的可执行文件. 随便放在那里, 我是把它放在了 ``${HOME}/pngquant/`` 下.
2. 如果是压缩一个文件, 我用的是 ``${HOME}/pngquant/pngquant 8 ${PATH_TO_YOUR_IMAGE} --quality 0-70 --output ${PATH_TO_YOUR_OUTPUT_IMAGE}`` 命令.
3. 虽然它支持批量压缩文件夹下的很多文件, 但是你都用 Python 写 wrapper 了, 还不如用 ``pathlib`` 选择文件, 然后用多线程批量压缩.

这里有一个 wrapper 的例子:

.. literalinclude:: ./example.py
   :language: python
