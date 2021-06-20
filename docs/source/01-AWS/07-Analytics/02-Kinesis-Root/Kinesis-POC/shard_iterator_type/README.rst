本 POC 是用于研究不同的 Iterator 对应着怎样的 Consumer 策略

- AT_SEQUENCE_NUMBER - Start reading from the position denoted by a specific sequence number, provided in the value StartingSequenceNumber .
- AFTER_SEQUENCE_NUMBER - Start reading right after the position denoted by a specific sequence number, provided in the value StartingSequenceNumber .
- AT_TIMESTAMP - Start reading from the position denoted by a specific time stamp, provided in the value Timestamp .
- TRIM_HORIZON - Start reading at the last untrimmed record in the shard in the system, which is the oldest data record in the shard.
- LATEST - Start reading just after the most recent record in the shard, so that you always read the most recent data in the shard.