Migration and Transfer
==============================================================================

- AWS Database Migration Service: Source Database -> Task on Replication Instance -> Target Database
- Data Sync
- Snowball: 100TB - PB级数据迁徙, Amazon 给你寄来一些 Snowball 机器, 然后用这些机器连接你数据中心中的电脑, 将你数据中心的数据, VM, Database 等全部 byte by byte 地拷贝到你 Snowball 中, 然后用卡车运到 AWS Data Center, 然后 AWS 帮你做数据迁徙.