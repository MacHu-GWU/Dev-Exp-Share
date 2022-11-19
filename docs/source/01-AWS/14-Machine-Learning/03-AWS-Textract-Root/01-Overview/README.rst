Amazon Textract Overview
==============================================================================
Keywords: AWS Textract, ORC, Form, Table, Data Extraction.


What is Textract
------------------------------------------------------------------------------
聊 Textract 之前我们先来聊 Optical character recognition (OCR), 这个有 100 多年历史的技术. OCR 就是用从图片中提取文本的技术, 底层的核心技术是训练好的机器学习目标识别模型. 市面上有很多开源的, 商用的 OCR 工具. 例如非常有名的免费的 Tesseract.

简单来说 Textract 就是一款由 AWS 维护的 OCR 产品, 而这个产品被打包成了 Web Service, 可以用 API 调用, 按使用量收费, 也可以跟其他的云服务整合在一起构成一个管道. 而且这个 OCR 不仅效果非常好, 还提供了文本所在图片上的位置数据, 这就使得很多用法从不可能变成了可能.

**但是**, Textract 的功能远远不止 OCR, 它还能分析文档, 从文档中提取结构化的数据, 进行分档分类, 提取表格数据, 分析收据金融数据.


Features
------------------------------------------------------------------------------
Textract 的核心功能:

- `Detecting Text <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-detecting.html>`_: 这就是简单的 OCR, 只负责提取文本. 输出结果是一个个的 Block, block 可以是 page, line, word, 不仅包含了在图片上的位置多边形数据, 还包含了 block 之间的逻辑关系.
- `Analyzing Documents <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html>`_: 在 OCR 之外提供了分析文档内容的功能, 目前支持 4 种分析目标:
    - text: 这个跟 OCR 一样
    - forms: 提取表单, 例如 W2, IRS 税表
    - tables: 提取二维表格数据
    - queries: 输入一段问题, 尝试给出回答, 就像 Google Search 一样
- `Analyzing Invoices and Receipts <https://docs.aws.amazon.com/textract/latest/dg/invoices-receipts.html>`_: 分析收据.
- `Analyzing Identity Documents <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-identity.html>`_: 分析 ID 卡, 例如 驾照, 身份证, 保险卡, 护照 等等.


其他应用场景
------------------------------------------------------------------------------
- 文档分类. 比如你有一堆 PDF 文件, 每个文件有很多页, 你想要分类每个 PDF 的每一页分别是什么文档, 然后根据分类结果对其进行后续处理. 这个用 Textract 将文档转化为 TXT, 然后用 Comprehend 构建一个 `Custom Document Classifier <https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html>`_ 即可.


Textract 文档摘要
------------------------------------------------------------------------------
AWS Textract 文档一大堆, 我们这里列出了一些最核心的文档.

- `Amazon Textract Response Objects <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-document-response.html>`_: Textract API 返回的对象是结构化的 JSON. 这篇文档介绍了这个 JSON 的具体结构, 以及每个 Key Value 代表的是什么含义, 如何解读这个对象.
    - Text Detection and Document Analysis Response Objects: https://docs.aws.amazon.com/textract/latest/dg/how-it-works-document-layout.html
    - Invoice and Receipt Response Objects: https://docs.aws.amazon.com/textract/latest/dg/expensedocuments.html
    - Identity Documentation Response Objects: https://docs.aws.amazon.com/textract/latest/dg/identitydocumentfields.html

- Data Type: https://docs.aws.amazon.com/textract/latest/dg/API_Types.html
- Block: https://docs.aws.amazon.com/textract/latest/dg/API_Block.html


参考资料
------------------------------------------------------------------------------
- What is Amazon Textract?: https://docs.aws.amazon.com/textract/latest/dg/what-is.html
- amazon-textract-textractor: https://github.com/aws-samples/amazon-textract-textractor
