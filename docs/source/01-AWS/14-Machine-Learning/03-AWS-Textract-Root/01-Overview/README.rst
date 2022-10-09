Amazon Textract Overview
==============================================================================
Keywords: AWS Textract


What is Textract
------------------------------------------------------------------------------
聊 Textract 之前我们先来聊 Optical character recognition (OCR), 这个有 100 多年历史的技术. OCR 就是用从图片中提取文本的技术, 底层的核心技术是训练好的机器学习目标识别模型. 市面上有很多开源的, 商用的 OCR 工具. 例如非常有名的免费的 Tesseract.

简单来说 Textract 就是一款由 AWS 维护的 OCR 产品, 而这个产品被打包成了 Web Service, 可以用 API 调用, 按使用量收费, 也可以跟其他的云服务整合在一起构成一个管道. 而且这个 OCR 不仅效果非常好, 还提供了文本所在图片上的位置数据, 这就使得很多用法从不可能变成了可能.

**但是**, Textract 的功能远远不止 OCR, 它还能分析文档, 从文档中提取结构化的数据, 进行分档分类, 提取表格数据, 分析收据金融数据.


Features
------------------------------------------------------------------------------
- `Detecting Text <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-detecting.html>`_: 这就是简单的 OCR, 只负责提取文本. 输出结果是一个个的 Block, block 可以是 page, line, word, 不仅包含了在图片上的位置多边形数据, 还包含了 block 之间的逻辑关系.
- `Analyzing Documents <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-analyzing.html>`_: 在 OCR 之外提供了分析文档内容的功能, 目前支持 4 种分析目标:
    - text: 这个跟 OCR 一样
    - forms: 提取表单, 例如 W2, IRS 税表
    - tables: 提取二维表格数据
    - queries: 输入一段问题, 尝试给出回答, 就像 Google Search 一样
- `Analyzing Invoices and Receipts <https://docs.aws.amazon.com/textract/latest/dg/invoices-receipts.html>`_: 分析收据.
- `Analyzing Identity Documents <https://docs.aws.amazon.com/textract/latest/dg/how-it-works-identity.html>`_: 分析 ID 卡, 例如 驾照, 身份证, 保险卡, 护照 等等.


参考资料
------------------------------------------------------------------------------
- What is Amazon Textract?: https://docs.aws.amazon.com/textract/latest/dg/what-is.html
