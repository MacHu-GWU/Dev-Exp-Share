CAP Theorem 定理
==============================================================================

CAP 定理是学术界公认的关于分布式系统的理论. 一个分布式系统通常会具有下面三个属性中的两种:

- Consistency: Every read receives the most recent write or an error (等同于所有节点访问同一份最新的数据副本)
- Availability: Every request receives a (non-error) response, without the guarantee that it contains the most recent write (每次请求都能获取到非错的响应, 但是不保证获取的数据为最新数据)
- Partition tolerance: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes (以实际效果而言, 分区相当于对通信的时限要求. 系统如果不能在时限内达成数据一致性, 就意味着发生了分区的情况, 必须就当前操作在C和A之间做出选择.)

根据定理, 分布式系统只能满足三项中的两项而不可能满足全部三项. 理解CAP理论的最简单方式是想象两个节点分处分区两侧. 允许至少一个节点更新状态会导致数据不一致, 即丧失了C性质. 如果为了保证数据一致性, 将分区一侧的节点设置为不可用, 那么又丧失了A性质. 除非两个节点可以互相通信, 才能既保证C又保证A, 这又会导致丧失P性质.
