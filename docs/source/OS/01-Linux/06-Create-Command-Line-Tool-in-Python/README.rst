Create Command Line Tool in Python
==============================================================================

通常情况下, 作为一个 Python 开发者, 要自己写的命令行工具, 你有三个选择:

1. 用 shell scripts 实现, 比如 pyenv 就是用的纯 shell script 实现. 但是 shell scripts 本身不是通用型编程语言, 所以有些复杂功能你要么精通 shell scripts, 要么用很复杂的方式实现, 导致可读性差.
2. 用 python 自带的库 argparse, 适用于输入输出简单的情况.
3. 用 python 里的 clicks 框架 (或者其他命令行工具框架) 创建你自己的命令行工具. 适用于复杂的命令行应用.
