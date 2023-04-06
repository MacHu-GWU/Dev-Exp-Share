.. _aws-step-function-faq:

FAQ
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, FAQ



AWS Step Function Pricing
------------------------------------------------------------------------------
收费的因素对于 Standard 和 Express 两种类型的 State Machine 是不同的:

- Standard 由于是长时间运行, 常用于 Async run, 它只按照在 State 之间的 transition (转移) 次数来计费. 也就是说你中键即使 Wait 了很久, Wait 的期间不会被计费.
- Express 由于是短时间运行, 常用于 Sync Run, 它只按照 Invoke 的次数, 以及 Duration + Memory (和 Lambda 相似) 来计费. 如果你有 Parallel 和 Map, 会有大量的 Payload, 那么这些 Payload 也会被计费.

Reference:

- AWS Step Functions Pricing: https://aws.amazon.com/step-functions/pricing/
- Building cost-effective AWS Step Functions workflows: https://aws.amazon.com/blogs/compute/building-cost-effective-aws-step-functions-workflows/


AWS Step Function Standard vs Express Type
------------------------------------------------------------------------------
Standard 主要是用于长时间运行的, 也符合 orchestration tool 的本质, 只能被 async execute, 按照 transition 的次数计费. 而 Express 主要用于短时间运行, 用完就走, 相当于是把一堆短时间运行的 worker 编排到一起, 可以被 async 和 sync execute, 按照 duration / memory 计费.

这里有几个主要指标:

- max duration:
    - standard: 1 year
    - express: 5 min
- execute:
    - standard: async only
    - express: async and sync

Reference:

- Standard vs Express (这里有个对比的表格): https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html
- start_execution: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_execution
- start_sync_execution: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_sync_execution
