Sublime Text是一款轻量级, 跨平台, 具有强大功能, 学习曲线平滑友好, 并对Python编程支持友好的文本编辑器软件。其强大的文本编辑功能和健壮的Package Control扩展包社区使得Sublime Text足够能成为全功能的Python IDE。由于Sublime Text 3对Python2和3的兼容和支持, 以及更强大的功能, 我们使用Sublime Text 3版本。

有一点值得注意的是, 脚本中不要在Console里Print太多的东西, 会占用非常多的资源(Console的功能并不如Eclipse强大)。比如下面这样的脚本就不要在Sublime Text中运行了:

.. code-block:: python

	from __future__ import print_function

	for i in range(1000000):
		print(i)

参考资料:

- 下载: http://www.sublimetext.com/3
- 官方简要文档: https://www.sublimetext.com/docs/3/index.html
- 非官方参考文档: http://docs.sublimetext.info/en/latest/index.html