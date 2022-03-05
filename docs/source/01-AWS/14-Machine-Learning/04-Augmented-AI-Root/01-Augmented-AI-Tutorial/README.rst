.. _aws-augmented-ai-root:

AWS Augmented AI Root
==============================================================================
Keywords: AWS Augmented AI, a2i, human in loop, HIL

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Augmented AI
------------------------------------------------------------------------------
A traditional Human-in-loop Workflow Example, credit card application use case:

1. **Digital Input**:

.. code-block:: python

    {
        "application_id": "a-127",
        "application_date": "2022-01-03",
        "apply_for": {
            "product_name": "bank of america, Customized cash rewards",
            "credit_line": 5000,
        }
        "ssn": "111-22-3333",
        "name": "James Bond",
        "resident_address": "123 st, New York, NY 10001",
        "job": "Software Engineer",
        "monthly_income": 15000,
        "last_six_month_income": [
            {"month": "2021-12", "income": 15000},
            {"month": "2021-11", "income": 15000},
            {"month": "2021-10", "income": 15000},
            {"month": "2021-09", "income": 9000},
            {"month": "2021-08", "income": 9000},
            {"month": "2021-07", "income": 9000},
        ],
    }

2. **Computational Output**:

.. code-block:: python

    {
        "application_id": "a-127",
        "approve": True,
    }

3. **Merge Input / Output data, generate a Human review request. Send the merged data to backend**.
4. **Reviewer login to internal system, click on the request**
    - You can create a Sagemaker GroundTruth Private Workforce team, and invite trusted worker to the team using the email. The login is automatically handled by AWS Cognito, the AWS Sign Up/ Sign in as service product.
    - You can also out source the project to AWS Public GroundTruth Workforce team. (be careful with PII data / Adult content)
5. **Convert merged data to a user-friendly UI**
    - A2I Task Template is a highly customizable HTML template, can render the merged data to HTML UI.
6. **Reviewer submit the data and finish the review**
    - Sagemaker GroundTruth Private Workforce provides an user friendly UI to browse the information, review the data and submit feedback.
7. **Send review data to target data location for further process**
    - A2I automatically send the HIL data to AWS S3 bucket in JSON format

在这个例子中我们可以看出, 在传统的 HIL 的流程中, 你需要额外管理一些东西:

1. 管理被授权 review 的人的 login, 以及对他们的行为进行追踪
2. 开发一个 UI, 供 reviewer 使用.
3. 根据要被 review 的 input / output 数据, 生成相应的 UI.
4. 在 UI 上提交的数据要被妥善储存.

而 A2I 的核心功能就是把这些通用的系统抽象出来, 打包成服务, 提供一些可扩展的接口, 供用户使用.

而在 ML 领域, 对于有些任务我们不能完全信任 ML 模型, 需要对一部分的结果进行人工修正. 例如在律师行业里 OCR 图片转文本, 金融领域Comprehend 对文字词组进行标注. 这种 ML 模型 + 人工协作的应用场景, 业内如果要搭建一套这样的系统, 成本还是不低的. 而 AWS Augmented AI 则是这样一套开箱即用的系统:

1. 对 ML 任务进行抽象, 将 ML 任务抽象为 Input Output.
2. 对人工进行抽象, 将人力资源抽象为 Workforce, 并基于 AWS Cognito 进行权限管理.
3. 对人工标注的 APP 进行抽象, 提供了一套可自定义的 GUI, GUI 模板的抽象叫做 Task Template.
4. 对何时触发人工标注进行抽象, 基于不同的 task 有不同的 metrics 可以用于定义 event, 触发人工标注 (Human in Loop)
5. 对输入输出数据进行抽象, 用 AWS S3 储存输入输出数据.
6. 对整个 Workflow 进行抽象 (Human Review Workflow)


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


Augmented AI Concepts
------------------------------------------------------------------------------
**Workers**

    真正执行 HIL review 的人. 通常是非技术人员. 有三种方式:

    1. 自己在 `GroundTruth <https://console.aws.amazon.com/sagemaker/groundtruth#/labeling-workforces>`_ 中创建 Private Workforce, 然后用 Email 邀请可信的人来做这个 Review 的工作, 通常是自己的员工.
    2. 使用 Amazon Mechanical Turk 外包服务, 让来自世界的 contractor 来帮你做这个工作.
    3. 使用 AWS Market Place 上的 Vendor, 让专业的人给你提供这个服务.

**Task Template**

    一个用 Shopify 开发的 Liquid HTML template engine 的 HTML 文件. 给定 Input Data, 就能 Render 出 HIL 要用的 UI. 由于是前端技术, 内嵌 图片, 视频, PDF 都是可以实现的, 并且扩展性很强.

**Human review workflow**

    Augmented AI 最顶层的抽象. 它把其他组件聚合在一起, 它包含如下信息:

    1. 名字
    2. 用于存放人工标注输出的 Output S3 dir
    3. 给 Human review workflow 用于和其他 AWS Service 通信的 IAM Role 权限
    4. 定义 Task Type, 目前原生支持 AWS Textract, AWS Rekognition. 以及允许自定义 Custom Task (这里涉及进一步的抽象)
    5. 如果是有 built-in integration 的服务, 则可以用模板自定义 Condition, 否则则需要自己在 trigger 的业务逻辑中定义.
    6. 由哪些 Workers 来处理这些 HIL
    7. 一个所有 HIL task 的列表, 可以看到这些 HIL 的状态

**HIL Task**

    被 Review 的最小单位. 同一个 task 可以被多个人处理.


Augmented AI Best Practice
------------------------------------------------------------------------------
1. 建议使用 Custom Task Template, 从而有更多的 Control.
2. 建议使用 AWS Lambda 来创建 HIL Task, 这个 Lambda 可以被各种上游计算结果触发. 例如 ML 的计算结果被 dump 到 S3 中, 就可以触发 AWS Lambda 来创建 HIL Task.
3. 建议为每个 Flow Definition 中的 Worker 一项设置使用 3 个以上的 Worker 对同一个 HIL Task 进行 Review, 这样能使用大多数人一致的结果来排查人工错误.
4. 建议使用 Dynamodb 来记录 HIL Task 与实际业务逻辑中的 ID 的对应关系, 以及 HIL Task 的状态.


Reference
------------------------------------------------------------------------------
- Create Custom Worker Task Templates: https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-custom-templates.html
- Creating Good Worker Instructions: https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-creating-good-instructions-guide.html
- Crowd HTML Elements Reference: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html
- Amazon A2I Output Data: https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-output-data.html
- Liquid Template Reference: https://shopify.github.io/liquid/
- Task Template Preview Tool: https://codepen.io/sagemaker_crowd_html_elements/pen/KKawYBm
- Python Liquid render: https://pypi.org/project/python-liquid/
