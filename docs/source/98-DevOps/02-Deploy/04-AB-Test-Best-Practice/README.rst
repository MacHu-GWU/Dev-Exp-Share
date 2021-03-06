.. _ab-test-best-practice:

AB Test Best Practice
==============================================================================

参考资料:

- 打造工业级推荐系统（八）：AB 测试平台的工程实现: https://www.infoq.cn/article/lCTiIpkrh-lPl9pitKhf

**为什么要做 AB 测试**:

1. 为评估产品优化效果提供科学的证据 (Proof your assumption)
2. 借助 AB 测试可以提升决策的说服力 (Convince stake holder)
3. AB 测试可以帮助提升用户体验和用户增长 (Improve user experience and increase customer)
4. AB 测试可以帮助提升公司变现能力

**什么时候需要 AB 测试**:

1. 必须是有大量用户的产品或者功能点
2. 进行 AB 测试的代价 (金钱 & 时间) 可以接受
3. 有服务质量提升诉求
4. 变量可以做比较好的精细控制

**AB 测试的应用场景**:

1. 算法类 (ML Algorithm)
2. 运营类 (Operation / Marketing)
3. UI 展示及交互类 (UI, User Conversion)

**AB 测试平台核心模块**:

1. 分组模块 (user splitting)
2. 业务接入模块 (service gateway)
3. 行为记录分析模块 (User behavior data collection and analysis)
4. 效果评估模块 (metrics evaluation)
5. 实验管理模块, 将上面的 4 个模块做成通用的接口, 供开发者, 业务人员, 数据分析人员使用 (experiment management)

**业界流行的 AB 测试架构实现方案**:

1. Client Side, 在客户端整合 AB 测试能力, 通过定制的 AB Test SDK 来处理 AB 测试业务
    - 好处: 客户端开发者比较方便, 调用接口即可,
    - 坏处: 如果公司有 PC, IOS, Android 多个平台的 SDK, 维护成本较大
2. Server Side, 在后端业务层增加相关组件来做 AB 测试
    - 好处: 模块化, Router 解决与 AB Test
    - 坏处: Route 是单点故障风险, Route 坏了, 不仅实验做不了, 而且服务都用不了
3. Application Code Level, 通过在算法业务层跟 AB 测试服务交互来实现 AB 测试能力，不需要前端和接口层做任何处理
    - 好处: 在业务中本身使用 AB 测试能力, 相当于 Feature Toggle
    - 坏处: 对业务代码入侵, 而且如果业务的语言不通, 你需要为不同的语言都开发一套 Feature Toggle, 维护比较难. 试验后会留下垃圾代码
