Kinesis Video Stream (KVS)
==============================================================================

.. contents::
    :local:


Reference: https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/what-is-kinesis-video.html

Kinesis Video Stream 的主要应用场景是视频监控. 换言之对于短期内上传的数据可以观看实时画面, 或是 Playback (使用 S3 实现存储层). Stream 中的视频数据不会保存很久, 一段时间后会被 Archive 到 S3 IA, `但仍然可以访问和 Playback <https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_Types_Amazon_Kinesis_Video_Streams_Archived_Media.html?shortFooter=true>`_.

注意: Kinesis的目标不是用来实现视频网站的!

**我们以大楼安全视频监控为例, 介绍如何使用 KVS 实现**:

你创建了 Kinesis Video Stream, 你就可以通过在你的 摄像机, 或是监控设备上安装 Producer Library (SDK), 将视频数据分割成 Fragment, 通过 Producer API 发送到 Stream. 在 Console 中你可以 Playback, 实时查看视频图像.

然后可以在你的监控中心电脑上的客户端软件中安装 Stream Parser Library (SDK) 查看实时监控图像, 以及使用 Consumer API, 调用指定时间段内的视频.

通过提供两套 API:

- Producer API: ``put media``
- Consumer API: ``get media``

两套客户端的 SDK:

- Producer Library (SDK): https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producer-sdk.html?shortFooter=true
- Stream Parser Library (SDK): https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/parser-library.html?shortFooter=true


Kinesis Concepts
------------------------------------------------------------------------------

- **Producer**: 可以是手机, 可以是摄像设备 (需要安装 AWS SDK)
- **Kinesis video stream**: 传输视频数据, 使其随时能被读取, 或以 Batch 的模式, 或以 on-demand 的模式. A resource that enables you to transport live video data, optionally store it, and make the data available for consumption both in real time and on a batch or ad hoc basis.
- **Consumer**:
    - **Kinesis Video Stream Parser Library**: 从视频数据中抽取所需要的时间段和帧. Enables Kinesis Video Streams applications to reliably get media from Kinesis video streams in a low-latency manner. Additionally, it parses the frame boundaries in the media so that applications can focus on processing and analyzing the frames themselves.


Kinesis Video Stream API
------------------------------------------------------------------------------

- Producer API: ``put media``
- Consumer API: ``get media``

- 从摄像头发从出去的数据, 看起来是这个样子: Media Metadata, Fragment1, Fragment2, Fragment3. 数据会被分块通过 Put Media API 发送到 Video Stream
- Stream 中每一个 Chunk 的数据看起来是这个样子的: Media Metadata, Kinesis Video Pre Metadata, Fragment, Kinesis Video Post Metadata.
- 总结: 视频数据的最小单位是 Fragment, 每个 Fragment 包含了 Media Metadata, Pre Metadata, Post Metadata. 实际的 App 其实是按照顺序获取 Fragment, 实现视频缓冲效果.


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



