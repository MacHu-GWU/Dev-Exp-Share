Manipulate PDF in Python
==============================================================================
- `PyPDF2 <https://pypi.org/project/PyPDF2/>`_: open source, free. 老牌 Python PDF 项目.
- `PyMuPDF <https://pypi.org/project/PyMuPDF/>`_: open source only, need to buy license for commercial project. 全面且强大, 基于 C++ 写的  `MuPDF <https://mupdf.com/>`_. 但是 Python 包自带用的是预编译的 MuPDF binary, 所以无需 yum, apt install. 美中不足就是商用需要 License
- `pdf2image <https://pypi.org/project/pdf2image/>`_: open source, free. 功能很简单, 将 PDF 转化为 Image 图片, 底层用的是 `popper <https://poppler.freedesktop.org/>`_ 这个 PDF Render 工具. 需要用 yum, apt install CLI 之后才能使用.
- `pdfminer <https://github.com/pdfminer/pdfminer.six>`_: MIT.


PyPDF2 Example:

.. literalinclude:: ./PyPDF2/test.py
   :language: python


PyMuPDF Example:

.. literalinclude:: ./PyMuPDF/test.py
   :language: python


pikepdf Example:

.. literalinclude:: ./pikepdf/test.py
   :language: python


pdf2image Example:

.. literalinclude:: ./pdf2image/test.py
   :language: python
