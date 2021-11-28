.. _aws-comprehend:

AWS Comprehend
==============================================================================



What is AWS Comprehend
------------------------------------------------------------------------------

Ref:

- https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html

- **Entities** – Amazon Comprehend returns a list of entities, such as people, places, and locations, identified in a document. For more information, see Detect Entities.

- **Key phrases** – Amazon Comprehend extracts key phrases that appear in a document. For example, a document about a basketball game might return the names of the teams, the name of the venue, and the final score. For more information, see Detect Key Phrases.

- **PII** – Amazon Comprehend analyzes documents to detect personal data that could be used to identify an individual, such as an address, bank account number, or phone number. For more information, see Detect Personally Identifiable Information (PII).

- **Language** – Amazon Comprehend identifies the dominant language in a document. Amazon Comprehend can identify 100 languages. For more information, see Detect the Dominant Language.

- **Sentiment** – Amazon Comprehend determines the emotional sentiment of a document. Sentiment can be positive, neutral, negative, or mixed. For more information, see Determine Sentiment.

- **Syntax** – Amazon Comprehend parses each word in your document and determines the part of speech for the word. For example, in the sentence "It is raining today in Seattle," "it" is identified as a pronoun, "raining" is identified as a verb, and "Seattle" is identified as a proper noun. For more information, see Analyze Syntax.


AWS Comprehend API
------------------------------------------------------------------------------

Ref:

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
- Sync API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.detect_entities
- Async API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.start_entities_detection_job

Comprehend 有两种 API 调用模式, Sync 和 Async.

对于 Sync 模式, 就是你调用了 API, 需要等 Comprehend 返回结果才能继续. 好处是方便, 并且返回速度快, 是 stateless 形式的调用. 缺点是 text 的大小不能超过 5000 bytes, 也就是 5KB.

对于 Async 模式, 就是你调用了 API, 就可以立刻返回. 等一段时间在 S3 Output Uri 处就会出现结果. 这个结果是以 ``s3_output_uri/${account_id}-${job_type}-${job_id}/output/output.tar.gz`` 的形式给你, 解压后是一个 Json 的纯文本文件. 还有一个问题是 Async 的调用需要在后台启用一些资源. 所以消耗的时间大约在 3 分钟作用, 元比手动将文本切割后调用 Sync API 的总和还多. 关于如何进行后续处理, 由于他的结果是一个单个的文件, 所以可以用 S3 Event Trigger