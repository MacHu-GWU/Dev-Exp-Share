.. _amazon-comprehend-custom-document-classification:

Custom Document Classification
==============================================================================
Keywords: Comprehend, Custom Document Classification, Classifier

简单来说, 这个服务就是你把文档中的 text 用 Textract 提取出来, 转化为纯文本, 然后把 换行符都替换掉, 使得文本只有一行. 然后创建一个 CSV 文件, 一列是文本本身, 一列是 Label. 然后调用 Comprehend API 训练模型, 训练好之后使用即可.

详细的例子请参考下面这个 Jupyter Notebook.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   custom-document-classification-example