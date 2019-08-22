# -*- coding: utf-8 -*-

import json


class StateMachineField:
    Comment = "Comment"
    StartAt = "StartAt"
    TimeoutSeconds = "TimeoutSeconds"
    States = "States"


class StateField:
    Type = "Type"
    Comment = "Comment"
    Next = "Next"
    Resource = "Resource"

    # Data Input Output
    InputPath = "InputPath"
    Parameters = "Parameters"
    ResultPath = "ResultPath"
    OutputPath = "OutputPath"

    # Choice State
    Choices = "Choices"
    Default = "Default"

    End = "End"
    Retry = "Retry"
    Catch = "Catch"
    Branches = "Branches"


class StateType:
    Pass = "Pass"
    Task = "Task"
    Choice = "Choice"
    Wait = "Wait"
    Succeed = "Succeed"
    Fail = "Fail"
    Parallel = "Parallel"


state_machine = {
    StateMachineField.Comment: "Fetch Amazon Stock Price, if it is greater than 100, notify me.",
    StateMachineField.StartAt: "Fetch Amazon Stock Price",
    StateMachineField.States: {
        "Fetch Amazon Stock Price": {
            StateField.Type: StateType.Task,
            StateField.Resource: "arn:aws:lambda:us-east-1:224233068863:function:step-func-example-get-amazon-stock-price",
            StateField.Next: "Send Notification or Not",
        },
        "Send Notification or Not": {
            StateField.Type: StateType.Choice,
            StateField.Choices: [
                {
                    "And": [
                        {
                            "Variable": "$.price",
                            "NumericGreaterThanEquals": 100,
                        },
                    ],
                    StateField.Next: "Notify Me",
                },
            ],
            StateField.Default: "Success",
        },
        "Notify Me": {
            StateField.Type: StateType.Task,
            StateField.Resource: "arn:aws:lambda:us-east-1:224233068863:function:step-function-example-notify-me",
            StateField.Parameters: {
                "amazon_stock_price.$": "$.price",
            },
            StateField.End: True,
        },
        "Success": {
            StateField.Type: StateType.Succeed,
        },
    }
}

js = json.dumps(state_machine, indent=4, sort_keys=True)
print(js)
