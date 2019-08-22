亚马逊状态机语言
==============================================================================

翻译: `Amazon States Language <https://states-language.net/spec.html>`_

Amazon States Language

This document describes a JSON-based language used to describe state machines declaratively. The state machines thus defined may be executed by software. In this document, the software is referred to as “the interpreter”.

Copyright © 2016 Amazon.com Inc. or Affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy of this specification and associated documentation files (the “specification”), to use, copy, publish, and/or distribute, the Specification) subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies of the Specification.

You may not modify, merge, sublicense, and/or sell copies of the Specification.

THE SPECIFICATION IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SPECIFICATION OR THE USE OR OTHER DEALINGS IN THE SPECIFICATION.​

Any sample code included in the Specification, unless otherwise specified, is licensed under the Apache License, Version 2.0.


.. contents:: 目录
    :depth: 2
    :local:


状态机的结构
------------------------------------------------------------------------------

我们用 JSON 对象来描述一个状态机.


Example: Hello World
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The operation of a state machine is specified by states, which are represented by JSON objects, fields in the top-level “States” object. In this example, there is one state named “Hello World”.


.. code-block:: python

    {
        "Comment": "A simple minimal example of the States language",
        "StartAt": "Hello World",
        "States": {
            "Hello World": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                "End": true
            }
        }
    }

When this state machine is launched, the interpreter begins execution by identifying the Start State. It executes that state, and then checks to see if the state is marked as an End State. If it is, the machine terminates and returns a result. If the state is not an End State, the interpreter looks for a “Next” field to determine what state to run next; it repeats this process until it reaches a Terminal State (Succeed, Fail, or an End State) or a runtime error occurs.

In this example, the machine contains a single state named “Hello World”. Because “Hello World” is a Task State, the interpreter tries to execute it. Examining the value of the “Resource” field shows that it points to a Lambda function, so the interpreter attempts to invoke that function. Assuming the Lambda function executes successfully, the machine will terminate successfully.

A State Machine is represented by a JSON object.


顶层关键字
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一个状态机 **必须** 有 ``States`` 关键字, 定义了多个具体的状态. 一个状态机是由多个状态组成的, 自然必须得有多个状态.

一个状态机 **必须** 有 ``StartAt`` 关键字, 对应的值必须是在 ``States`` 中定义了的某一个状态. 每个状态机, 有且只有一个起始状态.

一个状态机 **可以** 有 ``Comment`` 关键字, 对应的值简单地描述了这个状态机.

A State Machine MAY have a string field named “Version”, which gives the version of the States language used in the machine. This document describes version 1.0, and if omitted, the default value of “Version” is the string “1.0”.

A State Machine MAY have an integer field named “TimeoutSeconds”. If provided, it provides the maximum number of seconds the machine is allowed to run. If the machine runs longer than the specified time, then the interpreter fails the machine with a States.Timeout Error Name.


重要概念
------------------------------------------------------------------------------

状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

States are represented as fields of the top-level “States” object. The state name, whose length MUST BE less than or equal to 128 Unicode characters, is the field name; state names MUST be unique within the scope of the whole state machine. States describe tasks (units of work), or specify flow control (e.g. Choice).

Here is an example state that executes a Lambda function:

.. code-block:: python

    "HelloWorld": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
        "Next": "NextState",
        "Comment": "Executes the HelloWorld Lambda function"
    }


请注意:

所有的 State **必须** 有 ``Type`` 关键字. 定义了该状态是属于那种类型.

任何 State **可以** 有 ``Comment`` 关键字, 描述一下该状态是做什么的.

Most state types require additional fields as specified in this document.

只要状态的类型不是 ``Choice``, ``Succeed`` 和 ``Fail``, 都 **可以** 有 ``End`` 关键字, 值是一个布尔值. 在下文中, 我们用 ``Terminal State`` 来简称那些有 ``{"End": true}``, 或 ``{"Type:: "Succeed"}``, 或 ``{"Type:: "Fail"}`` 的状态.


状态转移
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

所有 ``状态`` 是通过 ``转移`` 而连接起来的. ``转移`` 定义了整个状态机的流程. 执行完一个不是 ``Terminal State`` 的 ``状态`` 后, 就会被 ``Next`` 关键字转移到下一个状态.

所有不是 ``Terminal State`` 的 ``状态`` 都必须有 ``Next`` 关键字. 除非它是 ``Choice`` 类型的 ``状态``. ``Next`` 关键字里的值对大小写敏感.

可以有多个 ``状态`` 的 ``Next`` 指向同一个 ``状态``.


时间戳
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

简单来说, 时间戳的格式必须是 ISO 8601 格式, 例如 ``2016-03-14T01:59:00Z``.

The Choice and Wait states deal with JSON field values which represent timestamps. These are strings which MUST conform to the RFC3339 profile of ISO 8601, with the further restrictions that an uppercase “T” character MUST be used to separate date and time, and an uppercase “Z” character MUST be present in the absence of a numeric time zone offset, for example “2016-03-14T01:59:00Z”.


数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

解释器通过在 ``状态`` 之间传递数据, 来动态控制状态机流程. 所有的数据都必须是 JSON.

When a state machine is started, the caller can provide an initial JSON text as input, which is passed to the machine's start state as input. If no input is provided, the default is an empty JSON object, {}. As each state is executed, it receives a JSON text as input and can produce arbitrary output, which MUST be a JSON text. When two states are linked by a transition, the output from the first state is passed as input to the second state. The output from the machine's terminal state is treated as its output.

For example, consider a simple state machine that adds two numbers together:

.. code-block:: python

    {
        "StartAt": "Add",
        "States": {
        "Add": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Add",
                "End": true
            }
        }
    }

假设 ``Add`` 的代码是这样的:

.. code-block:: javascript

    exports.handler = function(event, context) {
        context.succeed(event.val1 + event.val2);
    };

Then if this state machine was started with the input { "val1": 3, "val2": 4 }, then the output would be the JSON text consisting of the number 7.

The usual constraints applying to JSON-encoded data apply. In particular, note that:

Numbers in JSON generally conform to JavaScript semantics, typically corresponding to double-precision IEEE-854 values. For this and other interoperability concerns, see RFC 7159.

Standalone "-delimited strings, booleans, and numbers are valid JSON texts.


路径
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

这里的路径指的是 JSON 中的路径, 也叫 JsonPath. 是一个以 ``$`` 符号开头, 用来定位 JSON 中的某个值的一套语法.


参考路径
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Reference Path is a Path with syntax limited in such a way that it can only identify a single node in a JSON structure: The operators “@”, “,”, “:”, and “?” are not supported - all Reference Paths MUST be unambiguous references to a single value, array, or object (subtree).

For example, if state input data contained the values:

.. code-block:: python

    {
        "foo": 123,
        "bar": ["a", "b", "c"],
        "car": {
            "cdr": true
        }
    }

Then the following Reference Paths would return:

.. code-block:: javascript

    $.foo => 123
    $.bar => ["a", "b", "c"]
    $.car.cdr => true


Paths and Reference Paths are used by certain states, as specified later in this document, to control the flow of a state machine or to configure a state's settings or options.

Here are some examples of acceptable Reference Path syntax:

$.store.book
$.store\.book
$.\stor\e.boo\k
$.store.book.title
$.foo.\.bar
$.foo\@bar.baz\[\[.\?pretty
$.&Ж中.\uD800\uDF46
$.ledgers.branch[0].pending.count
$.ledgers.branch[0]
$.ledgers[0][22][315].foo
$['store']['book']
$['store'][0]['book']


输入输出数据的处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :local:

就如我们之前所说的, 数据是通过 JSON 来传输的. 但是有些状态可能只需要数据中的一小部分. 并且, 当一个状态受到另一个状态的输入, 并将其当做输入时, 当前状态所希望的输入的数据格式, 可能与收到的完全不同. 所以我们可以对输入进行一些处理. 同样的我们也可以对该状态的输出做一些处理.

这些 ``InputPath``, ``Parameters``, ``OutputPath``, ``ResultPath`` 关键字就是用来帮助我们做处理的. 任何除了 ``Fail State`` 以外的状态, 都 **可以** 有 ``InputPath`` 和 ``OutputPath``. 任何会产生结果的状态, 都 **可以** 有 ``ResultPath`` 和 ``Parameters``: Pass State, Task State, and Parallel State.

In this discussion, “raw input” means the JSON text that is the input to a state. “Result” means the JSON text that a state generates, for example from external code invoked by a Task State, the combined result of the branches in a Parallel State, or the value of the “Result” field in a Pass state. “Effective input” means the input after the application of InputPath and Parameters, and “effective output” means the final state output after processing the result with ResultPath and OutputPath.


``InputPath``, ``Parameters``, ``OutputPath``, ``DefaultPath``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. The value of “InputPath” MUST be a Path, which is applied to a State’s raw input to select some or all of it; that selection is used by the state, for example in passing to Resources in Task States and Choices selectors in Choice States.

2. “Parameters” may have any value. Certain conventions described below allow values to be extracted from the effective input and embedded in the Parameters structure. If the “Parameters” field is provided, its value, after the extraction and embedding, becomes the effective input.

3. The value of “ResultPath” MUST be a Reference Path, which specifies the raw input’s combination with or replacement by the state’s result.

4. The value of “OutputPath” MUST be a Path, which is applied to the state’s output after the application of ResultPath, producing the effective output which serves as the raw input for the next state.

Note that JsonPath can yield multiple values when applied to an input JSON text. For example, given the text::

    { "a": [1, 2, 3, 4] }

Then if the JsonPath $.a[0,1] is appplied, the result will be two JSON texts, 1 and 2. When this happens, to produce the effective input, the interpreter gathers the texts into an array, so in this example the state would see the input::

    [ 1, 2 ]

The same rule applies to OutputPath processing; if the OutputPath result contains multiple values, the effective output is a JSON array containing all of them.

The ResultPath field’s value is a Reference Path that specifies where to place the result, relative to the raw input. If the input has a field which matches the ResultPath value, then in the output, that field is discarded and overwritten by the state output. Otherwise, a new field is created in the state output.

If the value of InputPath is null, that means that the raw input is discarded, and the effective input for the state is an empty JSON object, {}. Note that having a value of null is different from the InputPath field being absent.

If the value of of ResultPath is null, that means that the state’s own raw output is discarded and its raw input becomes its result.

If the value of OutputPath is null, that means the input and result are discarded, and the effective output from the state is an empty JSON object, {}.


默认值
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Each of InputPath, Parameters, ResultPath, and OutputPath are optional. The default value of InputPath is “$”, so by default the effective input is just the raw input. The default value of ResultPath is “$”, so by default a state’s result overwrites and replaces the input. The default value of OutputPath is “$”, so by default a state’s effective output is the result of processing ResultPath.

Parameters has no default value. If it is absent, it has no effect on the effective input.

Therefore, if none of InputPath, Parameters, ResultPath, or OutputPath are supplied, a state consumes the raw input as provided and passes its result to the next state.


Input/Output Processing Examples
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Consider the example given above, of a Lambda task that sums a pair of numbers. As presented, its input is: ``{ "val1": 3, "val2": 4 }`` and its output is: 7.

Suppose the input is little more complex:

.. code-block:: python

    {
        "title": "Numbers to add",
        "numbers": { "val1": 3, "val2": 4 }
    }

Then suppose we modify the state definition by adding:

.. code-block:: python

    "InputPath": "$.numbers",
    "ResultPath": "$.sum"

And finally,suppose we simplify Line 4 of the Lambda function to read as follows: ``return JSON.stringify(total)``. This is probably a better form of the function, which should really only care about doing math and not care how its result is labeled.

In this case, the output would be:

.. code-block:: python

    {
        "title": "Numbers to add",
        "numbers": { "val1": 3, "val2": 4 },
        "sum": 7
    }

The interpreter might need to construct multiple levels of JSON object to achieve the desired effect. Suppose the input to some Task state is:

.. code-block:: python

    { "a": 1 }

Suppose the output from the Task is “Hi!”, and the value of the “ResultPath” field is “$.b.greeting”. Then the output from the state would be:

.. code-block:: python

    {
        "a": 1,
        "b": {
            "greeting": "Hi!"
        }
    }


Parameters
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The value of the ``Parameters`` field (after processing described below) becomes the effective input. Consider the following Task state:

.. code-block:: python

    "X": {
        "Type": "Task",
        "Resource": "arn:aws:swf:us-east-1:123456789012:task:X",
        "Next": "Y",
        "Parameters": {
            "first": 88,
            "second": 99
        }
    }

In this case, the effective input to the code identified in the Resource field would be the object with “first” and “second” fields which is the value of the “Parameters” field.

Values from the effective input can be inserted into the “Parameters” field with a combination of a field-naming convention and JsonPath.

If any JSON object within the value of Parameters (however deeply nested) has a field whose name ends with the characters “.$”, its value MUST be a Path. In this case, the Path is applied to the effective input and the result is called the Extracted Value.

If the path is legal but cannot be applied successfully the Interpreter fails the machine execution with an Error Name of “States.ParameterPathFailure”.

When a field name ends with “.$” and its value can be used to generate an Extracted Value as described above, the field is replaced within the Parameters value by another field whose name is the original name minus the “.$” suffix, and whose value is the Extracted Value.

Consider this example:

.. code-block:: python

    "X": {
        "Type": "Task",
        "Resource": "arn:aws:swf:us-east-1:123456789012:task:X",
        "Next": "Y",
        "Parameters": {
            "flagged": true,
            "parts": {
                "first.$": "$.vals[0]",
                "last3.$": "$.vals[3:]"
            }
        }
    }

Suppose that the input to the state is as follows:

.. code-block:: python

    {
        "flagged": 7,
        "vals": [0, 10, 20, 30, 40, 50]
    }

In this case, the effective input to the code identified in the Resource field would be as follows:

.. code-block:: python

    {
        "flagged": true,
        "parts": {
            "first": 0,
            "last3": [30, 40, 50]
        }
    }

Runtime Errors
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Suppose a state’s input is the string "foo", and its “ResultPath” field has the value “$.x”. Then ResultPath cannot apply and the Interpreter fails the machine with Error Name of “States.ResultPathMatchFailure”.


Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. contents::
    :local:

Any state can encounter runtime errors. Errors can arise because of state machine definition issues (e.g. the “ResultPath” problem discussed immediately above), task failures (e.g. an exception thrown by a Lambda function) or because of transient issues, such as network partition events.

When a state reports an error, the default course of action for the interpreter is to fail the whole state machine.


Error representation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Errors are identified by case-sensitive strings, called Error Names. The States language defines a set of built-in strings naming well-known errors, all of which begin with the prefix “States.”; see Appendix A.

States MAY report errors with other names, which MUST NOT begin with the prefix “States.”.


Retrying after error
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Task States and Parallel States MAY have a field named “Retry”, whose value MUST be an array of objects, called Retriers.

Each Retrier MUST contain a field named “ErrorEquals” whose value MUST be a non-empty array of Strings, which match Error Names.

When a state reports an error, the interpreter scans through the Retriers and, when the Error Name appears in the value of of a Retrier’s “ErrorEquals” field, implements the retry policy described in that Retrier.

An individual Retrier represents a certain number of retries, usually at increasing time intervals.

A Retrier MAY contain a field named “IntervalSeconds”, whose value MUST be a positive integer, representing the number of seconds before the first retry attempt (default value: 1); a field named “MaxAttempts” whose value MUST be a non-negative integer, representing the maximum number of retry attempts (default: 3); and a field named “BackoffRate”, a number which is the multiplier that increases the retry interval on each attempt (default: 2.0). The value of BackoffRate MUST be greater than or equal to 1.0.

Note that a “MaxAttempts” field whose value is 0 is legal, specifying that some error or errors should never be retried.

Here is an example of a Retry field which will make 2 retry attempts after waits of 3 and 4.5 seconds:

.. code-block:: python

    "Retry" : [
        {
            "ErrorEquals": [ "States.Timeout" ],
            "IntervalSeconds": 3,
            "MaxAttempts": 2,
            "BackoffRate": 1.5
        }
    ]

The reserved name “States.ALL” in a Retrier’s “ErrorEquals” field is a wild-card and matches any Error Name. Such a value MUST appear alone in the “ErrorEquals” array and MUST appear in the last Retrier in the “Retry” array.

Here is an example of a Retry field which will retry any error except for “States.Timeout”, using the default retry parameters.

.. code-block:: python

    "Retry" : [
        {
          "ErrorEquals": [ "States.Timeout" ],
          "MaxAttempts": 0
        },
        {
          "ErrorEquals": [ "States.ALL" ]
        }
    ]

If the error recurs more times than allowed for by the “MaxAttempts” field, retries cease and normal error handling resumes.


Complex retry scenarios
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A Retrier’s parameters apply across all visits to that Retrier in the context of a single state execution. This is best illustrated by example; consider the following Task State:

.. code-block:: python

    "X": {
        "Type": "Task",
        "Resource": "arn:aws:swf:us-east-1:123456789012:task:X",
        "Next": "Y",
        "Retry": [
            {
                "ErrorEquals": ["ErrorA", "ErrorB"],
                "IntervalSeconds": 1,
                "BackoffRate": 2,
                "MaxAttempts": 2
            },
            {
                "ErrorEquals": ["ErrorC"],
                "IntervalSeconds": 5
            }
        ],
        "Catch": [
            {
                "ErrorEquals": ["States.ALL"],
                "Next": "Z"
            }
        ]
    }

Suppose that this task fails four successive times, throwing Error Names “ErrorA”, “ErrorB”, “ErrorC”, and “ErrorB”. The first two errors match the first retrier and cause waits of one and two seconds. The third error matches the second retrier and causes a wait of five seconds. The fourth error would match the first retrier but its “MaxAttempts” ceiling of two retries has already been reached, so that Retrier fails, and execution is redirected to the “Z” state via the “Catch” field.

Note that once the interpreter transitions to another state in any way, all the Retrier parameters reset.


Fallback 状态
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Task 和 Parallel 状态 **可能** 会有一个叫做 ``Catch`` 的关键字. 它的值 **必须** 一个对象的列表, 我们称之为 ``Catchers``.

Task States and Parallel States MAY have a field named “Catch”, whose value MUST be an array of objects, called Catchers.

Each Catcher MUST contain a field named “ErrorEquals”, specified exactly as with the Retrier “ErrorEquals” field, and a field named “Next” whose value MUST be a string exactly matching a State Name.

When a state reports an error and either there is no Retry field, or retries have failed to resolve the error, the interpreter scans through the Catchers in array order, and when the Error Name appears in the value of a Catcher’s “ErrorEquals” field, transitions the machine to the state named in the value of the “Next” field.

The reserved name “States.ALL” appearing in a Retrier’s “ErrorEquals” field is a wild-card and matches any Error Name. Such a value MUST appear alone in the “ErrorEquals” array and MUST appear in the last Catcher in the “Catch” array.


Error output
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

When a state reports an error and it matches a Catcher, causing a transfer to another state, the state’s result (and thus the input to the state identified in the Catcher’s “Next” field) is a JSON object, called the Error Output. The Error Output MUST have a string-valued field named “Error”, containing the Error Name. It SHOULD have a string-valued field named “Cause”, containing human-readable text about the error.

A Catcher MAY have an “ResultPath” field, which works exactly like a state’s top-level “ResultPath”, and may be used to inject the Error Output into the state’s original input to create the input for the Catcher’s “Next” state. The default value, if the “ResultPath” field is not provided, is “$”, meaning that the output consists entirely of the Error Output.

Here is an example of a Catch field that will transition to the state named “RecoveryState” when a Lambda function throws an unhandled Java Exception, and otherwise to the “EndMachine” state, which is presumably Terminal.

Also in this example, if the first Catcher matches the Error Name, the input to “RecoveryState” will be the original state input, with the Error Output as the value of the top-level “error-info” field. For any other error, the input to “EndMachine” will just be the Error Output.

"Catch": [
  {
    "ErrorEquals": [ "java.lang.Exception" ],
    "ResultPath": "$.error-info",
    "Next": "RecoveryState"
  },
  {
    "ErrorEquals": [ "States.ALL" ],
    "Next": "EndMachine"
  }
]
Each Catcher can specifiy multiple errors to handle.

When a state has both Retry and Catch fields, the interpreter uses any appropriate Retriers first and only applies the a matching Catcher transition if the retry policy fails to resove the error.


State Types
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

As a reminder, the state type is given by the value of the “Type” field, which MUST appear in every State object.


Table of State Types and Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many fields can appear in more than one state type. The table below summarizes which fields can appear in which states. It excludes fields that are specific to one state type.

States
Pass	Task	Choice	Wait	Succeed	Fail	Parallel
Type	Required	Required	Required	Required	Required	Required	Required
Comment	Allowed	Allowed	Allowed	Allowed	Allowed	Allowed	Allowed
InputPath, OutputPath	Allowed	Allowed	Allowed	Allowed	Allowed		Allowed
Parameters	Allowed	Allowed					Allowed
ResultPath	Allowed	Allowed					Allowed
One of: Next or "End":true	Required	Required		Required			Required
Retry, Catch		Allowed					Allowed


Pass 状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

关键字 ``"Type":"Pass"``

 simply passes its input to its output, performing no work. Pass States are useful when constructing and debugging state machines.

A Pass State MAY have a field named “Result”. If present, its value is treated as the output of a virtual task, and placed as prescribed by the “ResultPath” field, if any, to be passed on to the next state. If “Result” is not provided, the output is the input. Thus if neither “Result” nor “ResultPath” are provided, the Pass state copies its input through to its output.

Here is an example of a Pass State that injects some fixed data into the state machine, probably for testing purposes.

.. code-block:: python

    "No-op": {
        "Type": "Pass",
        "Result": {
            "x-datum": 0.381018,
            "y-datum": 622.2269926397355
        },
        "ResultPath": "$.coords",
        "Next": "End"
    }

Suppose the input to this state were as follows:

.. code-block:: python

    {
      "georefOf": "Home"
    }

Then the output would be:

.. code-block:: python

    {
        "georefOf": "Home",
        "coords": {
            "x-datum": 0.381018,
            "y-datum": 622.2269926397355
        }
    }


Task 状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

关键字 ``"Type": "Task"``. 执行 ``Resource`` 中的 Lambda 函数.

Here is an example:

.. code-block:: python

    "TaskState": {
        "Comment": "Task State example",
        "Type": "Task",
        "Resource": "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
        "Next": "NextState",
        "TimeoutSeconds": 300,
        "HeartbeatSeconds": 60
    }

A Task State MUST include a “Resource” field, whose value MUST be a URI that uniquely identifies the specific task to execute. The States language does not constrain the URI scheme nor any other part of the URI.

Tasks can optionally specify timeouts. Timeouts (the “TimeoutSeconds” and “HeartbeatSeconds” fields) are specified in seconds and MUST be positive integers. If provided, the “HeartbeatSeconds” interval MUST be smaller than the “TimeoutSeconds” value.

If not provided, the default value of “TimeoutSeconds” is 60.

If the state runs longer than the specified timeout, or if more time than the specified heartbeat elapses between heartbeats from the task, then the interpreter fails the state with a States.Timeout Error Name.


Choice 状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Choice state (identified by "Type":"Choice") adds branching logic to a state machine.

A Choice state state MUST have a “Choices” field whose value is a non-empty array. Each element of the array is called a Choice Rule - an object containing a comparison operation and a “Next” field, whose value MUST match a state name.

The interpreter attempts pattern-matches against the Choice Rules in array order and transitions to the state specified in the “Next” field on the first Choice Rule where there is an exact match between the input value and a member of the comparison-operator array.

Here is an example of a Choice state, with some other states that it transitions to.

.. code-block:: python

    "ChoiceStateX": {
        "Type": "Choice",
        "Choices": [
            {
                "Not": {
                    "Variable": "$.type",
                    "StringEquals": "Private"
                },
                "Next": "Public"
            },
            {
                "And": [
                    {
                        "Variable": "$.value",
                        "NumericGreaterThanEquals": 20
                    },
                    {
                        "Variable": "$.value",
                        "NumericLessThan": 30
                    }
                ],
                "Next": "ValueInTwenties"
            }
        ],
        "Default": "DefaultState"
    },

    "Public": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Foo",
        "Next": "NextState"
    },

    "ValueInTwenties": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Bar",
        "Next": "NextState"
    },

    "DefaultState": {
        "Type": "Fail",
        "Cause": "No Matches!"
    }

In this example, suppose the machine is started with an input value of:

.. code-block:: python

    {
        "type": "private",
        "value": 22
    }

Then the interpreter will transition to the “ValueInTwenties” state, based on the “value” field.

Each choice rule MUST contain exactly one field containing a comparison operator. The following comparison operators are supported:

StringEquals

StringLessThan

StringGreaterThan

StringLessThanEquals

StringGreaterThanEquals

NumericEquals

NumericLessThan

NumericGreaterThan

NumericLessThanEquals

NumericGreaterThanEquals

BooleanEquals

TimestampEquals

TimestampLessThan

TimestampGreaterThan

TimestampLessThanEquals

TimestampGreaterThanEquals

And

Or

Not

For each of these operators, the field’s value MUST be a value of the appropriate type: String, number, boolean, or Timestamp.

The interpreter scans through the Choice Rules in a type-sensitive way, and will not attempt to match a numeric field to a string value. However, since Timestamp fields are logically strings, it is possible that a field which is thought of as a time-stamp could be matched by a “StringEquals” comparator.

Note that for interoperability, numeric comparisons should not be assumed to work with values outside the magnitude or precision representable using the IEEE 754-2008 “binary64” data type. In particular, integers outside of the range [-(253)+1, (253)-1] might fail to compare in the expected way.

The values of the “And” and “Or” operators MUST be non-empty arrays of Choice Rules that MUST NOT contain “Next” fields; the “Next” field can only appear in a top-level Choice Rule.

The value of a “Not” operator MUST be a single Choice Rule, that MUST NOT contain “Next” fields; the “Next” field can only appear in a top-level Choice Rule.

Choice states MAY have a “Default” field, which will execute if none of the Choice Rules match. The interpreter will raise a run-time States.NoChoiceMatched error if a “Choice” state fails to match a Choice Rule and no “Default” transition was specified.

Choice states MUST NOT be End states.


Wait 状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Wait state (identified by "Type":"Wait") causes the interpreter to delay the machine from continuing for a specified time. The time can be specified as a wait duration, specified in seconds, or an absolute expiry time, specified as an ISO-8601 extended offset date-time format string.

For example, the following Wait state introduces a ten-second delay into a state machine:

"wait_ten_seconds" : {
  "Type" : "Wait",
  "Seconds" : 10,
  "Next": "NextState"
}
This waits until an absolute time:

"wait_until" : {
  "Type": "Wait",
  "Timestamp": "2016-03-14T01:59:00Z",
  "Next": "NextState"
}
The wait duration does not need to be hardcoded. Here is the same example, reworked to look up the timestamp time using a Reference Path to the data, which might look like { "expirydate": "2016-03-14T01:59:00Z" }:

"wait_until" : {
    "Type": "Wait",
    "TimestampPath": "$.expirydate",
    "Next": "NextState"
}
A Wait state MUST contain exactly one of ”Seconds”, “SecondsPath”, “Timestamp”, or “TimestampPath”.


Succeed 状态
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Succeed State (identified by "Type":"Succeed") terminates a state machine successfully. The Succeed State is a useful target for Choice-state branches that don't do anything but terminate the machine.

Here is an example:

"SuccessState": {
  "Type": "Succeed"
}

Because Succeed States are terminal states, they have no “Next” field.


Fail State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Fail State (identified by "Type":"Fail") terminates the machine and marks it as a failure.

Here is an example:

"FailState": {
          "Type": "Fail",
          "Error": "ErrorA",
          "Cause": "Kaiju attack"
}
A Fail State MUST have a string field named “Error”, used to provide an error name that can be used for error handling (Retry/Catch), operational, or diagnostic purposes. A Fail State MUST have a string field named “Cause”, used to provide a human-readable message.

Because Fail States are terminal states, they have no “Next” field.


Parallel State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Parallel State (identified by "Type":"Parallel") causes parallel execution of "branches".

Here is an example:

"LookupCustomerInfo": {
  "Type": "Parallel",
  "Branches": [
    {
      "StartAt": "LookupAddress",
      "States": {
        "LookupAddress": {
          "Type": "Task",
          "Resource":
            "arn:aws:lambda:us-east-1:123456789012:function:AddressFinder",
          "End": true
        }
      }
    },
    {
      "StartAt": "LookupPhone",
      "States": {
        "LookupPhone": {
          "Type": "Task",
          "Resource":
            "arn:aws:lambda:us-east-1:123456789012:function:PhoneFinder",
          "End": true
        }
      }
    }
  ],
  "Next": "NextState"
}

A Parallel state causes the interpreter to execute each branch starting with the state named in its “StartAt” field, as concurrently as possible, and wait until each branch terminates (reaches a terminal state) before processing the Parallel state's “Next” field. In the above example, this means the interpreter waits for “LookupAddress” and “LookupPhoneNumber” to both finish before transitioning to “NextState”.

In the example above, the LookupAddress and LookupPhoneNumber branches are executed in parallel.

A Parallel State MUST contain a field named “Branches” which is an array whose elements MUST be objects. Each object MUST contain fields named “States” and “StartAt” whose meanings are exactly like those in the top level of a State Machine.

A state in a Parallel state branch “States” field MUST NOT have a “Next” field that targets a field outside of that “States” field. A state MUST NOT have a “Next” field which matches a state name inside a Parallel state branch’s “States” field unless it is also inside the same “States” field.

Put another way, states in a branch’s “States” field can transition only to each other, and no state outside of that “States” field can transition into it.

If any branch fails, due to an unhandled error or by transitioning to a Fail state, the entire Parallel state is considered to have failed and all the branches are terminated. If the error is not handled by the Parallel State, the interpreter should terminate the machine execution with an error.

The Parallel state passes its input (potentially as filtered by the “InputPath” field) as the input to each branch’s “StartAt” state. it generates output which is an array with one element for each branch containing the output from that branch. There is no requirement that all elements be of the same type.

The output array can be inserted into the input data using the state’s “ResultPath” field in the usual way.

For example, consider the following Parallel State:

"FunWithMath": {
  "Type": "Parallel",
  "Branches": [
    {
      "StartAt": "Add",
      "States": {
        "Add": {
          "Type": "Task",
          "Resource": "arn:aws:swf:::task:Add",
          "End": true
        }
      }
    },
    {
      "StartAt": "Subtract",
      "States": {
        "Subtract": {
          "Type": "Task",
          "Resource": "arn:aws:swf:::task:Subtract",
          "End": true
        }
      }
    }
  ],
  "Next": "NextState"
}
If the “FunWithMath” state was given the JSON array [3, 2] as input, then both the “Add” and “Subtract” states would receive that array as input. The output of “Add” would be 5, that of “Subtract” would be 1, and the output of the Parallel State would be a JSON array:

[ 5, 1 ]
If any branch fails, due to an unhandled error or by transitioning to a Fail state, the entire Parallel state is considered to have failed and all the branches are terminated. If the error is not handled by the Parallel State, the interpreter should terminate the machine execution with an error.

Appendices
------------------------------------------------------------------------------


Appendix A: Predefined Error Codes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code	Description
States.ALL
A wild-card which matches any Error Name.

States.Timeout
A Task State either ran longer than the “TimeoutSeconds” value, or failed to heartbeat for a time longer than the “HeartbeatSeconds” value.

States.TaskFailed
A Task State failed during the execution.

States.Permissions
A Task State failed because it had insufficient privileges to execute the specified code.

States.ResultPathMatchFailure
A state’s “ResultPath” field cannot be applied to the input the state received.

States.ParameterPathFailure
Within a state’s “Parameters” field, the attempt to replace a field whose name ends in “.$” using a Path failed.

States.BranchFailed
A branch of a Parallel state failed.

States.NoChoiceMatched
A Choice state failed to find a match for the condition field extracted from its input.