.. _git-commands-cheatsheet:

Git Commands Cheatsheet (Git 命令速查)
==============================================================================

.. contents:: Table of Content
    :depth: 1
    :local:


``git clone``
------------------------------------------------------------------------------

- clone master: ``git clone https://github.com/MacHu-GWU/learn_git-project``. This command usually used for download source code.
- clone specific branch (``release1``): ``git clone -b release1 https://github.com/MacHu-GWU/learn_git-project``. This command usually used for developing new features.
- clone specific branch at specific commit hash. This command usually used in CI/CD environment to clone specific version of the code::

    git clone https://github.com/MacHu-GWU/learn_git-project
    cd learn_git-projects
    git fetch --force origin "release1:remotes/origin/release1"
    git reset --hard e5581a5b32f20922509dec25c87b3247648010e5
    git checkout -B release1
    git reset --hard e5581a5b32f20922509dec25c87b3247648010e5


``git branch``
------------------------------------------------------------------------------

- list local branch: ``git branch``
- list local branch: ``git branch -l``
- list remote branch: ``git branch -r``
- list all branch: ``git branch -a``
- create a new branch (``feature1``) based on current branch: ``git branch feature1``
- rename a branch (from ``feature1`` to ``feature1/v1``): ``git branch -m feature1 feature1/v1``
- delete a branch (``feature1``): ``git branch -d feature1``


``git checkout``
------------------------------------------------------------------------------

``checkout`` usually for switching to the state of other branch or a specific version of commit.

- switch to ``feature1`` branch: ``git checkout feature1``. It is used to switch between existing branches.
- create and switch to ``feature1`` branch: ``git checkout -b feature1``. It is just a shortcut of ``git branch feature1; git checkout feature1``.
- checkout a remote branch from: ``git checkout -b feature1 origin/feature1``. This command usually used for start working from a state of remote branch.


``git push``
------------------------------------------------------------------------------

- push a local branch to remote if it is not exists on remote: ``git push -u origin feature1``. This command usually used when you want to publish a new branch to remote.
- push changes on current branch to remote: ``git push``


``git pull``
------------------------------------------------------------------------------

``pull`` usually for pulling updates on remote to local, and merge files on local. Unlike ``fetch``, it pulls changes and merge.

- pull latest code of this branch from remote: ``git pull``


``git fetch``
------------------------------------------------------------------------------

``fetch`` usually for pulling updates on remote to local. Unlike ``pull``, it doesn't merge.
