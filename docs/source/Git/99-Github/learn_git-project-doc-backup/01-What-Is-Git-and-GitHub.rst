What is Git and GitHub?
==============================================================================

Git是一个分布式的版本控制系统。GitHub是目前最流行的开源项目的代码托管平台, 只支持Git作为版本控制的系统。


什么是版本控制系统?
------------------------------------------------------------------------------
在软件开发的过程中, 如果是单人开发, 我们经常会希又望查看我们过去做了哪些更改(Commit), 或是希望回滚(Rollback)到代码库过去的某一个状态。而在团队协作开发过程中, 我们希望能够将多人的贡献在同一个代码库上进行汇总(Merge), 并准确查看哪些人做了哪些修改。如果多个人同时对一个文件进行了修改, 则需要一个管理员的角色对冲突进行解决(Conflit Resolve), 这个人通常承担了代码审查的角色(Code Review)。而有的时候在一个版本的基础上, 有一些开发者想在此基础上做一些修改, 把该项目变成另一个新项目, 这叫做分支(Branch)。而Git就是能解决这些问题的一个系统。

市面上比较流行的开源版本控制系统有CVS, SVN, Vesta; 闭源的有微软的TFS等。

Git和其他版本控制的系统最大的区别就是, Git是一个分布式的系统, 支持本地Commit; 而传统的Version Control都需要每个开发者在执行Clone, Commit, Push的时候联网。而Git只需要在Clone和Push的时候联网, 其他时候每个可以在本地Commit, 然后最后再在服务器上Merge。

一些学习Git的参考资料:

- Git the simple guide, no deep shit: http://rogerdudler.github.io/git-guide/index.zh.html
- Understanding Git Conceptually: https://www.sbf5.com/~cduan/technical/git/
- 专为设计师而写的GitHub快速入门教程: http://developer.51cto.com/art/201407/446249.htm


GitHub好在那里?
------------------------------------------------------------------------------

GitHub就好像是将Git搬到了云上, 免去了开发者自己搭建服务器的麻烦。并且每个人的GitHub账号是一个社交网络中的节点。使得互联网上互不认识的人的团队协作开发变得异常轻松, 这也是GitHub团队所宣称的: 让开发变得社交起来!

天下没有免费的午餐, GitHub给我们提供了免费的服务使用, 而我们要为 **免费** 付出的代价就是, 将自己的代码 **开源**。如果你想要让自己的代码私有, 或是作为企业代码库使用, 那么就需要交纳一定的费用。而免费的服务刺激了开源, 使得开发者们更加活跃起来, 让开发者们在合作的碰撞中, 持续创造出更好的作品。
