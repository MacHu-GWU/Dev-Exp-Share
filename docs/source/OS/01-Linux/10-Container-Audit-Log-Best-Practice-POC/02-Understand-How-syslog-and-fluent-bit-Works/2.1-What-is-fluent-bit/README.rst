What is fluent-bit
==============================================================================

From official doc:

    Fluent Bit is a Fast and Lightweight Log Processor, Stream Processor and Forwarder for Linux, OSX, Windows and BSD family operating systems. It has been made with a strong focus on performance to allow the collection of events from different sources without complexity.

Fluent-bit doesn't generate any log, and it is not the end-consumer of log in most of the cases. It is a middle ware connecting different common log creation tools such as rsyslog, collectd. It allows you to easily configure how do you want to process / filter / aggregate the log, and eventually send to common output such as datadog, elk, splunk, AWS S3 / Cloudwatch.

Fluent-bit Data Pipeline (https://docs.fluentbit.io/manual/concepts/data-pipeline/input) explains how's the data flows from its generation to its consumption via Fluent-bit.

Key concepts (https://docs.fluentbit.io/manual/concepts/key-concepts) are:

- input
- filter
- processor
- buffer
- output

fluent-bit plugins integrates many common log input and outputs. Basically, a logging pipeline based on fluent-bit is simply different combination of input | processor | output. To understand the configuration for different input | output, you can find answers here https://docs.fluentbit.io/manual/pipeline/inputs, https://docs.fluentbit.io/manual/pipeline/outputs.
