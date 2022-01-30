Smart Open 是一个非常优秀的文件 IO 库.

对于 S3 Read 操作, 由于 S3 API 是一个 stream reader, 所以可以用 bytes.io.find(delimiter) 来找到 line delimiter, 从而实现每次只读取一部分数据到内存. **也就是说 S3 object 只要是纯文本不是 big binary 或者压缩文件, 你就可以使用很少的内存处理很大的文件**.

对于 S3 Write 操作, 由于 S3 API 不支持 Stream Write, 所以 Smart Open 也做不到一次性只用比较少的内存一次写入一点点以节约内存. Smart Open 本质还是将数据写入 IO buffer, 然后一次性写入 S3. **也就是说 S3 object 占用多少内存, 你就需要使用多少内存**.
