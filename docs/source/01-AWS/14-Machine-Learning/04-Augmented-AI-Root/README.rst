.. _aws-augmented-ai-root:

AWS Augmented AI Root
==============================================================================

Ref:

- Using Amazon Augmented AI for Human Review: https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html


Amazon A2I Use Case Examples
------------------------------------------------------------------------------

The following examples demonstrate how you can use Amazon A2I to integrate a human review loop into your ML application. For each of these examples, you can find a Jupyter Notebook that demonstrates that workflow in Use Cases and Examples Using Amazon A2I.

- Use Amazon A2I with Amazon Textract – Have humans review important key-value pairs in single-page documents or have Amazon Textract randomly sample and send documents from your dataset to humans for review.
- Use Amazon A2I with Amazon Rekognition – Have humans review unsafe images for explicit adult or violent content if Amazon Rekognition returns a low-confidence score, or have Amazon Rekognition randomly sample and send images from your dataset to humans for review.
- Use Amazon A2I to review real-time ML inferences – Use Amazon A2I to review real-time, low-confidence inferences made by a model deployed to a SageMaker hosted endpoint and incrementally train your model using Amazon A2I output data.
- Use Amazon A2I with Amazon Comprehend – Have humans review Amazon Comprehend inferences about text data such as sentiment analysis, text syntax, and entity detection.
- Use Amazon A2I with Amazon Transcribe – Have humans review Amazon Transcribe transcriptions of video or audio files. Use the results of transcription human review loops to create a custom vocabulary and improve future transcriptions of similar video or audio content.
- Use Amazon A2I with Amazon Translate – Have humans review low-confidence translations returned from Amazon Translate.
- Use Amazon A2I to review tabular data – Use Amazon A2I to integrate a human review loop into an ML application that uses tabular data.


Augmented AI 是一个什么样的服务, 解决了什么问题
------------------------------------------------------------------------------
在 ML 领域, 对于有些任务我们不能完全信任 ML 模型, 需要对一部分的结果进行人工修正. 例如在律师行业里 OCR 图片转文本, 金融领域Comprehend 对文字词组进行标注. 这种 ML 模型 + 人工协作的应用场景, 业内如果要搭建一套这样的系统, 成本还是不低的. 而 AWS Augmented AI 则是这样一套开箱即用的系统:

1. 对 ML 任务进行抽象, 将 ML 任务抽象为 Input Output.
2. 对人工进行抽象, 将人力资源抽象为 Workforce, 并基于 AWS Cognito 进行权限管理.
3. 对人工标注的 APP 进行抽象, 提供了一套可自定义的 GUI, GUI 模板的抽象叫做 Task Template.
4. 对何时触发人工标注进行抽象, 基于不同的 task 有不同的 metrics 可以用于定义 event, 触发人工标注 (Human in Loop)
5. 对输入输出数据进行抽象, 用 AWS S3 储存输入输出数据.
6. 对整个 Workflow 进行抽象 (Human Review Workflow)


How Augmented AI Works?
------------------------------------------------------------------------------
**Human review workflow**

    Augmented AI 最顶层的抽象叫做 Human review workflow. 它包含如下信息:

    1. 名字
    2. 用于存放人工标注输出的 Output S3 dir
    3. 给 Human review workflow 用于和其他 AWS Service 通信的 IAM Role 权限
    4. 定义 Task Type, 目前原生支持 AWS Textract, AWS Rekognition. 以及允许自定义 Custom Task (这里涉及进一步的抽象)
    5. 定义 Condition,