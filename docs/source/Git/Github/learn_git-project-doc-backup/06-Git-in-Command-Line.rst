Git in Command Line
==============================================================================

在开发环境中, 我们通常会用图形化的Git客户端. 而在Linux远程服务器环境中, 我们并不会在远程环境中进行开发, 通常只是需要Pull代码, 然后进行打包, 部署之类的事情, 所以常用到的命令不不会很多, 掌握以下的命令基本就够用了.

- ``$ git init``: create new git repo.
- ``$ git clone``: clone code repo and all its history to local.
- ``$ git branch``: list all local branches.
- ``$ git branch -r``: list all remote branches.
- ``$ git branch -a``: list all local and remote branches.
- ``$ git checkout {branch}``: switch to xxx branch, if not exists, will create a new one.
- ``$ git checkout -``: switch back to last branch.
- ``$ git fetch {remote}``: fetch remote code change to local.


Reference
------------------------------------------------------------------------------

- Git Reference: https://git-scm.com/docs
- 常用 Git 命令清单: http://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html



