All in One Interview Cheatsheet
==============================================================================

1. b
------------------------------------------------------------------------------

c
------------------------------------------------------------------------------

Story BackLog
------------------------------------------------------------------------------


2022-06-27 AWS DLA Bridge Water Design Lab - Step Out of Comfort Zone and Pick Up Skill Fast as Required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Situation

    在 AWS Data Lab 做 Data Lab Architect 的时候, 接待了一个大客户 Bridgewater. 他们想做一个内部的企业文档搜索的 App. 客户和我本身都是搜索技术的专家, 也熟悉业内通用的技术 OpenSearch. 但是他们想了解 AWS 的新技术 Kendra, 是不是能满足他们的需求, 并能减少他们的 Technique Effort.

    虽然我也是搜索技术的专家, 但是我对 Kendra 没有任何了解. 我如何能在 2 个礼拜内成为 Kendra 的 Subject Matter Expert, Propose 一个 Solution, 并 Convince 客户使用 Kendra.

Task

    我需要在 2 个礼拜内, 但在这个回答中我想重点说我是如何 Pick Up Skill 的.

    1. 成为 SME
    2. Propose Solution
    3. Convince 客户

Action

    1. 成为 SME:
        - 我先分析客户作为搜索技术专家, 为什么需要我. 因为客户对 AWS Eco 不熟悉, 而我是 AWS 的专家, 并且有很多 Internal Resource 可以问问题. 所以我要多 Leverage Internal Resource 来 Pickup.
        - 其次我对 Knowledge Gap 进行拆分. 搜索技术的核心有以下三点. 我只要将传统技术是如何做到这三点的, 与 Kendra 做对比, 我就能有一个大概的理解了.
            - 数据如何存进去
            - 数据如何搜出来
            - 对数据访问的权限管理
        - 为了将我对 Kendra 的知识转换为一个 Production Ready System, 我需要 Hands on build 一个系统. 我 Based on 我以前用传统 OpenSearch 技术做过的 Search App 的 project, 用 Kendra 重新做了一遍. 这样我可以专注于 Kendra 和传统技术的 Delta, 而无需浪费精力在准备数据, 设计架构上.
    2. Propose Solution
        - 我首先分析关键点是什么. 一个 Solution 的关键是 设计 和 验证. 在很短的时间内 验证 一个复杂系统是最主要的难点.
        - 我利用了我以前自己开发的 data faker 框架, 可以用来 simulate 跟客户 production 环境中类似的巨量的数据流. 这样我就能专注在搭建系统, 解决问题上, 而无需在准备数据上浪费时间.
        - 我利用了我以前自己开发的 MicroService deployment automation tool 可以让我专注于业务逻辑, 而节省了大量时间在部署上.
    3. Convince 客户
        - 我首先分析关键点是什么. 在客户看到一个 Solution 的 Architect Diagram 之后, 无论我们怎么解释每个 Component 的功能, Document 做的多么的 Fancy, 客户都不可能完全信服. 而作为一个 Meeting, 我们不可能给客户看 Code Editor, 因为大部分的客户都不能 digest code.
        - 我有 Data Scientist 的背景. 在 Data Scientist 的领域写论文, 他们喜欢用 Jupyter Notebook 这种既能写 pretty document, 展现 diagram 和 chart, 也能 interactively 展现代码. 用 Jupyter Notebook 写出来的论文可以被 peer 轻易的 reproduce 实验结果. 我用这种方式把客户的 concern 抽象成 combination of input / output / logic branch, 并用最少的代码, 以 interactive 的形式展现 output 是如何跟着 input 变化的. 客户非常喜欢这种形式, 他们可以临时提出新问题, 并且立刻就能验证.
        - 我是我们 AWS Data Lab 第一个这么做的人, 我把这种方式做成了 Template, 在内部推广开, 培训了 5 个 DLA, 使他们 从 L4 promote 到了 L5.

Result

    1. 这次的 Design Lab 非常成功, 我获得了 5/5 Customer Satisfaction (CSAT). 客户决定 moving forward 去用我的 solution build 一个系统. 这将会给我们带来 1.2M / Y revenue
    2. 客户, 以及 AWS customer account 都给我发来了 accolade, 感谢我做的 contribution
    3. 我提出的这种 Convince 客户的 method 提高了我们 Design Lab 整体的 CSAT. 并且为 AWS 培养了 5 个 L4 -> L5 的 Data Lab Architect.


2022-06-27 AWS DLA Bridge Water Design Lab - Convince Customer That has Very Strong Opinion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Situation

    在 AWS Data Lab 做 Data Lab Architect 的时候, 接待了一个大客户 Bridgewater. 他们想做一个内部的企业文档搜索的 App. 客户和我本身都是搜索技术的专家, 也熟悉业内通用的技术 OpenSearch. 但是他们想了解 AWS 的新技术 Kendra, 是不是能满足他们的需求, 并能减少他们的 Technique Effort.

    来自 Bridgewater 的团队的 4 个人的两个 Leader 都是来自于 Google 的 Staff Engineer, 本身是搜索技术的专家. 但他们对 AWS Kendra 这个产品并不了解, 并且对 Google 的那一套搜索技术有很强的 bias. 我的 Conclusion 是 they should use Kendra for their search app not from pure engineering perspective. 但是要想 convince 这个客户会很难.

Task

    我需要在为期 2 天, 一共 8 小时的 Meeting 中, convince 客户使用 AWS Kendra 是他们的 UseCase 的最佳选择.

Action

    1. 分析这里的关键.
        - 客户本身是搜索技术的专家, 客户自然的会将 Kendra 与 Google 的搜索技术进行比较
        - 我掌握的客户需求信息不全, 客户随时可能在 Meeting 的时候提出任何没有准备的问题
        - 客户是 Engineer 背景, 他们觉得 talk is cheap, show me the code
    2. 我的准备工作.
        - 不能仅仅了解 Kendra 的搜索技术, 还要知道 alternative Google Search techniques, 如果我们不知道 Google 对应的技术, 客户是不会信服的.
        - 我需要准备一个 Interactive Shell, 预先 setup 好 document 和 Kendra 的连接, 这样客户提出的任何细节问题, 我可以用 code 当场展示不同的 input 如何产生不同的 output. 我决定用 Jupyter Notebook 来做这件事.
        - 我需要让客户信服我是一个 Very knowledgeable 的 engineer, 自然他们会更相信我的 judgement. 我说服客户也会更容易. 所以我需要用我的 engineer skill 证明我的实力, 我们是在 talking in the same language. 于是我基于我做的大量的 OpenSource project 的 template, 做了一个 Kendra based search app POC. 客户表示我的工作超过了他们的语气, 我的工作他们自己做可能要几个月, 所以他们非常相信我的 judgement

Result

    1. 这次的 Design Lab 非常成功, 我获得了 5/5 Customer Satisfaction (CSAT). 客户决定 moving forward 去用我的 solution build 一个系统. 这将会给我们带来 1.2M / Y revenue
    2. 客户, 以及 AWS customer account 都给我发来了 accolade, 感谢我做的 contribution


2022-06-07 AWS DLA College Board Design Lab - Accomplish a Very important job with Very Limited Timeline
------------------------------------------------------------------------------
Situation

    在 AWS Data Lab 做 Data Lab Architect 的时候, 有一个 DLA 在做 Design Lab 的前一天病了, 并且由于 Account Team 的 delay, 本应该有的 2-3 个跟客户的 preparation call 我们一次都没有做, 我们什么信息都没有. Schedule 已经被 Delay 2 次了, 我们不能再 Delay 了, 不然很可能会失去这个即将使用 Neptune Graph Database 的客户. 由于我在 Data Lab 以善于处理极大的不确定性的情况, 所以 Account Team, Project Manager 以及我的 Manager 找到我希望我能接手这个 Lab.

Task

    我面临的情况是, 平时需要 2 周准备, 跟客户开 3 次会了解情况和需求. 而我下午 1 点接到请求, 第二天下午 1 点就要做 lab 了, 目的是给客户做出 Solution Design, 不失去这个客户. 并且我只有一个非常 rough 的信息, 客户想要一个 Data Lineage and Data Traffic Monitoring 的系统, 客户的 Data 系统是什么, Traffic 是怎么样的, 对于 Lineage 和 traffic monitoring 的定义是什么我完全不知道.

Action

    1. 分析这里的关键
        - 缺少信息
        - 不确定性大
        - 客户已经 Delay 了几次有点 frustrated, 临时换 DLA 让客户很 concern
    2. 首先解决缺少信息的问题. 现在没有机会跟客户 meeting 了解需求了, 我只能从 Account Team 他们跟客户以前开过会的人里获得有限的信息. 重点是了解客户的需求的大方向, 了解到最关键的挑战是他们的 Data Catalog 数量很多, 并且在不断变化. 以及了解客户 Delay 多次, 不满意的原因, 是一直没有找到有合适 Engineer Skill 的 DLA.
    3. 第二解决不确定性大. 通常的 Design Lab 的 preparation 是从用户的 UseCase spread out 出去, 找到很多的 challenge, 然后一个一个的解决. 而我们现在没有这些信息, 不可能这么做. 于是我决定我在晚上围绕着已有的信息, 做了一个 Top-Down 的 framework, 这个 framework 很复杂, 能解决几乎所有的问题, 但是根据客户的需求我们要做很多取舍. 因为我认为从一个 Comprehensive Framework 然后根据用户的需求 converge 成一个具体的 System, 这种模式我能更好的控制 Conversation 和 Expectation. 避免用户想要的太多, 而我没有足够的准备时间去一一解决这个问题. 这个方法的问题是如果我的 framework off the track 就完蛋了. 所以我非常小心的设计这个 framework 使得它能更 general 一点, 以适应不同的情况, 并给出了 option 1, 2, 3.
    4. 第三解决客户不是很高兴. 这是客户第一次跟 AWS 做 Data Lab, 就遇到了多次 Delay. 我需要在解决客户的问题的同时, 保持一个更快的 response time. 这个 Lab 做完之后, 我 prioritize 了我写 lab report 的时间, 更快的交付了 Lab Artifacts. 在 2 个月内定义了 3 个 post lab activity, 并且都进行了 Lead. 让用户觉得等待是值得的.

Result

    1. 客户最终决定使用我 Propose 的 Neptune 方案来 Track 他们的 Data Catalog. 继续使用 AWS 的 Big Data Eco system.
    2. 在 3 个月后客户又继续做了 Build Lab, moving to production with AWS.


2022-05-12 AWS DLA Cox-Auto Design Lab -
------------------------------------------------------------------------------
Situation

Task

Action

Result
