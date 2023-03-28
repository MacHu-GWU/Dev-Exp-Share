.. _amazon-comprehend-overview:

Amazon Comprehend Overview
==============================================================================
Keywords: Amazon Comprehend Overview


What is Amazon Comprehend
------------------------------------------------------------------------------
Comprehend 是 AWS 下的一款全托管式的文本理解的 "机器学习模型即服务" 产品. 它的核心功能份两类:

1. 一类是预构建模型 (built-in Model), 也就是亚马逊已经训练好的模型, 你只要调用 API 用即可.
2. 另一类是允许用户提供数据 (Custom Model), 亚马逊系统算法和模型托管, 用你的数据训练一个属于你的模型.

此外, 对于 自定义模型, Comprehend 提供托管服务. 不像通常的机器学习模型需要用容器部署, 你训练好以后可以直接部署为 Endpoint, 然后调用那个 API Endpoint 来使用这个模型进行 real-time prediction. 当然这是由额外的费用的. 如果你不部署 Endpoint, 那么你只能用 Async / Batch 的模型调用训练好的模型.

Ref:

- https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html


Features
------------------------------------------------------------------------------
预构建模型功能:

- **Entities**
    - Amazon Comprehend returns a list of entities, such as people, places, and locations, identified in a document. For more information, see Detect Entities.
    - 从文本中提取 Entity, 例如 人, 地点, 日期, 货币金额 等
- **Key phrases**
    – Amazon Comprehend extracts key phrases that appear in a document. For example, a document about a basketball game might return the names of the teams, the name of the venue, and the final score. For more information, see Detect Key Phrases.
    - 根据上下文从文本中提取关键短语. 例如与球赛相关的文章, 球队的名字就是关键短语.
- **PII**
    – Amazon Comprehend analyzes documents to detect personal data that could be used to identify an individual, such as an address, bank account number, or phone number. For more information, see Detect Personally Identifiable Information (PII).
    - 从文本中提取身份信息, 例如名字, 社会安全号, 护照号 等.
- **Language**
    – Amazon Comprehend identifies the dominant language in a document. Amazon Comprehend can identify 100 languages. For more information, see Detect the Dominant Language.
    - 鉴别文本的语言. 英语, 法语, 西班牙语, 中文, 日文, 韩文等, Comprehend 支持 100 多种语言.
- **Sentiment**
    – Amazon Comprehend determines the emotional sentiment of a document. Sentiment can be positive, neutral, negative, or mixed. For more information, see Determine Sentiment.
    - 鉴别文档的情感偏向, 正面, 负面, 中立, 还是都有.
- **Syntax**
    – Amazon Comprehend parses each word in your document and determines the part of speech for the word. For example, in the sentence "It is raining today in Seattle," "it" is identified as a pronoun, "raining" is identified as a verb, and "Seattle" is identified as a proper noun. For more information, see Analyze Syntax.
    - 语义词法分析, 分析主谓宾, 形容词, 副词等.
- **Topic Model**
    - You can use Amazon Comprehend to examine the content of a collection of documents to determine common themes. For example, you can give Amazon Comprehend a collection of news articles, and it will determine the subjects, such as sports, politics, or entertainment. The text in the documents doesn't need to be annotated.
    - 文本主题模型 (底层用的是 LDA). 例如 CNN 新闻稿的主题分类.

自定义模型功能:

- `Custom classification <https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html>`_: 自定义的文本分类模型. 包含两种模型:
    - multi class: 一个文档只有一个类, 例如表格. 是 W2 表格就不可能是 W9 表格. 类标签是互斥的.
    - multi label: 一个文档可以有多个 Label, 例如新闻稿, 一个新闻稿可以有多个主题.
- `Custom entity recognition <https://docs.aws.amazon.com/comprehend/latest/dg/custom-entity-recognition.html>`_: 这是为了补足预构建模型中 Entity detection 太过通用的问题. 你对于你自己业务相关的文档可以定义一些 entity, 然后训练一个专用的模型.


Documentations
------------------------------------------------------------------------------
Comprehend 的文档太多了, 我们这里列出了一些常用的, 最核心的文档.

- 介绍文档:
- API 文档:
    - `boto3 comprehend API <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#comprehend>`_: 大部分的文档都有三个版本, 一个是 Sync 的版本, 通常只支持很少的数据量. 一个是 Async 的版本. 还有一个是 Batch 的版本. 例如 ``detect_entities``, ``start_entities_detection_job``, ``batch_detect_entities`` 都是用来 detect entities 的.
        - detect_entities
        - detect_key_phrases
        - detect_dominant_language
        - detect_syntax
        - detect_sentiment
        - detect_targeted_sentiment
        - start_topics_detection_job


AWS Comprehend API
------------------------------------------------------------------------------

Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
- Sync API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.detect_entities
- Async API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.start_entities_detection_job

Comprehend 有两种 API 调用模式, Sync 和 Async.

对于 Sync 模式, 就是你调用了 API, 需要等 Comprehend 返回结果才能继续. 好处是方便, 并且返回速度快, 是 stateless 形式的调用. 缺点是 text 的大小不能超过 5000 bytes, 也就是 5KB.

对于 Async 模式, 就是你调用了 API, 就可以立刻返回. 等一段时间在 S3 Output Uri 处就会出现结果. 这个结果是以 ``s3_output_uri/${account_id}-${job_type}-${job_id}/output/output.tar.gz`` 的形式给你, 解压后是一个 Json 的纯文本文件. 还有一个问题是 Async 的调用需要在后台启用一些资源. 所以消耗的时间大约在 3 分钟作用, 远比手动将文本切割后调用 Sync API 的总和还多. 关于如何进行后续处理, 由于他的结果是一个单个的文件, 所以可以用 S3 Event Trigger