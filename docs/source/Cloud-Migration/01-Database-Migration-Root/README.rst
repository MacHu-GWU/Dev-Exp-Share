Database Migration Guide
==============================================================================

- Oracle数据库迁移到AWS云的方案: https://aws.amazon.com/cn/blogs/china/oracle-database-migration/
- 使用AWS的数据库迁移DMS服务: https://aws.amazon.com/cn/blogs/china/migrating-dms/
- 如何利用 AWS DMS 轻松迈出数据库上云第一步，看这一篇就够了: https://zhuanlan.zhihu.com/p/47104594


数据库迁徙项目中不同的需求
------------------------------------------------------------------------------

在做一个数据库迁徙项目之前, 你需要考虑以下重要的项目需求:

**按照数据库是否停机 (难度从简单到难排列, 下同)**:

1. 可以停机, 那么 dump/load 的方案变得可行. 因为此方案简单, 但是耗时长.
2. 不可以停机, 业务不能中断. 那么只能先迁徙好, 并对新数据库进行测试, 然后进行切换.

**按照数据库的系统是否相同**:

1. 两者相同, 例如都是 PSQL or MySQL
2. 两者不同, 例如从 Oracle 到 AWS Aurora; 字符集, 数据类型, 索引都可能不同.
3. 两者的底层设计不同, 例如从 RDBMS 到 MongoDB; 非常复杂, 实践中很少会这么做.

**按照数据表的 Schema 是否相同**:

1. 两者完全相同, 表的数量, column definition, constrain, association 都一样.
2. 两者有细微的不同.
3. 两者有巨大不同.


实践
------------------------------------------------------------------------------

- 必须要做演习: 演习是说在跟 source database 类似的环境中建立一个数据规模差不太多的数据库, 然后模拟一些 read / write 然后对这个模拟数据库进行迁徙. 保证你的迁徙方法可行.
- 必须要做测试: 在迁徙之后, 需要使用 application code 对其进行测试, 保证迁徙后的数据库可用.
