Use SmartGit With GitHub in Ubuntu
==================================
`GitHub <https://github.com/>`_ 是目前最流行, 对用户最友好的云Git代码库托管商。而为了免去使用Git命令行的痛苦, GitHub在Windows和MacOS下都有客户端软件, 但是在Ubuntu系统下没有客户端软件。所以我们就需要使用第三方的Git客户端软件。个人觉得 `SmartGit <http://www.syntevo.com/smartgit/>`_ 是在这其中最好用的。


1. Create a Repository
----------------------
由于GitHub的Repository中有一些文件是GitHub系统中特殊的文件。所以既然要使用GitHub, 那么就最好使用 `GitHub客户端 <https://desktop.github.com/>`_ 或者使用 `GitHub代码库创建向导 <https://github.com/new>`_ ( `帮助文档在此 <https://help.github.com/articles/create-a-repo/>`_ ) 来创建代码库。这样会有步骤帮助用户创建GitHub的特殊文件。而如果使用Git或者其他第三方客户端创建, 就不会有这些特殊的GitHub文件的步骤。所以在Ubuntu系统中我们的选择是在GitHub的网页上创建我们的代码库。如果你的代码库已经在GitHub上, 则可以跳过此步骤。


2. Clone to Local Workspace
---------------------------
当你在网页上已经添加了Readme文件, 并进行了第一次Commit之后。就可以将代码库Clone到本地进行编辑了。

SmartGit使用你的GitHub Personal Access Token进行身份验证。进行了身份验证之后就有足够的权限对你GitHub账户上的代码库进行操作了。你可以在 https://github.com/settings/tokens 这里设置你的Token, 并设置你的权限。**建议关闭Token的Delete权限**, 防止使用客户端程序删除整个代码库。

点击SmartGit的: Menu -> Repository -> Clone, 在弹出的对话框中选择Remote Git or SVN Repository -> Provider -> Github.com -> 选择你的代码库 -> 选择你的本地Workspace路径, 一路Next -> Finish。

现在你在GitHub上的代码就被Clone到本地了。


3. Make Some Change and Commit to Remote
----------------------------------------
在开发过程中, 对于代码库而言, 我们的所有操作可以归类为以下三种:

1. 添加一个新文件。
2. 删除一个旧文件。
3. 对已有的文件进行修改。

以我们刚创建的test project为例。我们应该有一个LICENSE文件, 一个README.rst文件。那么就让我们:

1. 添加一个新的NewFile.rst文件, 随便打一些内容。
2. 删除LICENSE文件。
3. 修改README.rst文件, 随便写一些内容。

于是在SmartGit客户端中, 我们可以看见新添加的文件被标记为Untracked, 被删除的文件被标记为Missing, 被修改的文件被标记为Modified。

然后我们可以点击Commit按钮, 将我们新增的文件添加到Repository中, 然后在Commit Message中填入一些说明信息, 说明你这次的改动内容。Message的第一行会被作为标题, 所以第一行通常写日期信息和一行简短的话说明这次的改动。最后可以点击Commit and Push在本地进行Commit, 然后Push到远端服务器上。当然你也可以仅仅在本地进行Commit, 待你需要的时候再一次性Push到远端服务器上, 但个人不推荐这么做。因为一旦进行Commit, 那么Git打包文件中就已经包含了这次的版本信息, 延迟Push并不能带来任何空间的节约, **所以既然Commit了, 就同步到服务器上保存, 绝对是一个明智的选择**。

**由于笔者技术有限, Branch和Merge的部分没有进行足够的研究, 这部分内容就留到以后更新吧**。