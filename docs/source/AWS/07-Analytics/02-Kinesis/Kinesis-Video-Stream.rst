Kinesis Video Stream
==============================================================================

Reference: https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/what-is-kinesis-video.html

- Producer: 可以是手机, 可以是摄像设备 (需要安装 AWS SDK)
- Kinesis video stream: 传输视频数据, 使其随时能被读取, 或以 Batch 的模式, 或以 on-demand 的模式. A resource that enables you to transport live video data, optionally store it, and make the data available for consumption both in real time and on a batch or ad hoc basis.
- Consumer:
    - Kinesis Video Stream Parser Library: 从视频数据中抽取所需要的时间段和帧. Enables Kinesis Video Streams applications to reliably get media from Kinesis video streams in a low-latency manner. Additionally, it parses the frame boundaries in the media so that applications can focus on processing and analyzing the frames themselves.


Kinesis Video Stream API
------------------------------------------------------------------------------

- Producer API: ``put media``
- Consumer API: ``get media``

- 从摄像头发从出去的数据, 看起来是这个样子: Media Metadata, Fragment1, Fragment2, Fragment3. 数据会被分块通过 Put Media API 发送到 Video Stream
- Stream 中每一个 Chunk 的数据看起来是这个样子的: Media Metadata, Kinesis Video Pre Metadata, Fragment, Kinesis Video Post Metadata.


Kinesis Video Stream Parser Library
------------------------------------------------------------------------------

只有 Java 客户端

- StreamingMkvReader: 从 MKV 中流式读取视频, 也就是跳到中间.
- FragmentMetadataVisitor: 获得 FragmentMetadata
- OutputSegmentMerger: 将 Fragment 合并
- KinesisVideoExample: 一个教学例子, 教你使用 Kinesis Video Stream Parer Library


Monitoring Kinesis Video Streams
------------------------------------------------------------------------------

- Monitoring Kinesis Video Streams Metrics with **CloudWatch**
- Logging Kinesis Video Streams API Calls with AWS **CloudTrail**



