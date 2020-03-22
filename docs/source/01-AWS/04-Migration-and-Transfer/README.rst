Migration and Transfer
==============================================================================

从原有的自建数据中心和机房中将 数据, 应用, 架构 迁徙上云 是作为客户最关心事情. 而云供应商为了吸引客户, 也提供了很多成熟的解决方案帮助用户迁徙.

- AWS Database Migration Service (DMS): 数据库迁徙服务 Source Database -> Task on Replication Instance -> Target Database
- AWS Server Migration Service (SMS): 服务器迁徙服务, 进行比特级的复制, 然后在云上创建新的数据库.
- Data Sync: 通过在你的机器上安装客户端, 然后将数据同步到 AWS 账户中.
- Snowball: 100TB - PB级数据迁徙, Amazon 给你寄来一些 Snowball 机器, 然后用这些机器连接你数据中心中的电脑, 将你数据中心的数据, VM, Database 等全部 byte by byte 地拷贝到你 Snowball 中, 然后用卡车运到 AWS Data Center, 然后 AWS 帮你做数据迁徙.

.. autotoctree::
    :maxdepth: 1
