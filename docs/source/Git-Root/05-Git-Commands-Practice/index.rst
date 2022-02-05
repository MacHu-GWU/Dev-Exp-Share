.. _git-commands-practice:

Git Commands Practice (Git 命令行练习)
==============================================================================

In this tutorial, a git repo named ``learn_git-project`` will be created. It is placed in ``$HOME/Documents/GitHub`` directory. Then we will clone this repo to two different locations to simulate two people are doing development all together, which are ``$HOME/Documents/GitHub1/learn_git-project`` and ``$HOME/Documents/GitHub2/learn_git-project``.

This is how we simulate development in this tutorial:

- Suppose people **Alice** works on GitHub1, **Bob** works on GitHub2. And **Cathy** is the code reviewer and also the code owner.
- For any new features, it creates a text file named ``feature/f1.txt``, ``feature/f2.txt``. The content of the text file is the feature change version id of the feature. For example if the content of ``f1.txt`` is ``2``, it means it is the second version of ``feature1``.
- For any new releases, it creates a text file named ``release/r1.txt``, ``release/r2.txt``. The content of the text file is the release change version id. For example if the content of ``r1.txt`` is ``2``, it means it is the second version of ``release1``.

.. contents:: Table of Content
    :depth: 1
    :local:


1. Create / Initialize a new Repo
------------------------------------------------------------------------------

GOAL:

    The code owner Cathy wants to create and initialize a repo for the projects.

First, Log in to your GitHub, click ``New Repository``, fill in ``learn_git-project`` to ``Repository Name``.

You can choose to "Initialize this repository with a README", otherwise, you need to:

.. code-block:: bash

    # go to the repo directory
    cd ~/Documents/Github
    mkdir learn_git-project
    cd learn_git-project

    # initialize the repo and add your first commit
    git init
    git add README.md
    git commit -m "first commit"

    # ``remote`` represent a remote git server, you need to tell git
    # which remote server you are interactive with.
    git remote add origin https://github.com/MacHu-GWU/learn_git-project.git
    git push -u origin master


2. Alice add a New Feature
------------------------------------------------------------------------------

GOAL:

    Alice got assigned to develop a new feature called f1.

.. code-block:: bash

    # clone repo to local
    git clone https://github.com/MacHu-GWU/learn_git-project.git

    # create a new branch called feature1 based on the current branch
    # mostly master
    git branch feature1/v1

    # switch to feature1 branch
    git checkout feature1/v1

    # start applying changes
    mkdir features
    echo "1" > features/f1.txt

    # you have to tell git the files you want to track changes
    git add features/f1.txt

    # view difference of this commit, seems good
    git diff

    # commit
    git commit -m "add f1.txt"

    # give current branch a name for remote branch
    # and push changes on branch to remote
    # -u means upstream, origin is the default remote server alias
    git push -u origin feature1/v1

Then Cathy will do the code review and merge it to master.


3. Bob Creates a Release from master
------------------------------------------------------------------------------

GOAL:

    The team release every two weeks on Friday, now it's Thursday of the second week. Bob is about to release and deploy to production. In ``release`` branch, Bob should not add any new feature and only perform documentation and clean up. For Trunk Base Development, no commits should be done from ``release`` branch. Changes on ``release`` branch should only done by ``cherry-pick`` from other branch.

.. code-block:: bash

    # clone repo to local
    git clone https://github.com/MacHu-GWU/learn_git-project.git

    # create and switch to new branch for releasing
    git checkout -b release1


4. Alice add a Documentation for feature1
------------------------------------------------------------------------------

GOAL:

    After #3, Alice wants to add some documents for the feature1.


.. code-block:: bash

    # switch to the branch
    git checkout feature1/v1

    # apply some changes
    echo "1 # v1 description" > features/f1.txt

    # commit
    git add features/f1.txt
    git commit -m "add description to feature1 v1"

    # push to remote
    git push

And the code review passed, and code merged into master.


5. Bob cherry pick Commits from master
------------------------------------------------------------------------------

GOAL:

    Since Alice has added some documents after the first release. Bob wants to pickup those documentation into the release.

.. code-block:: bash

    # view the most recent commits
    git checkout master
    git log

    # cherry-pick specific commits and merge into the release1 branch
    git checkout release1
    git cherry-pick c14875cafd8f9586460438354312b6e7412cba60

    # push to remote
    git push

Then release again from the ``release1`` branch.


6. Hot fix a Release
------------------------------------------------------------------------------

GOAL:

    Some bugs are observed, Bob wants to fix those bugs and re-deploy.

Similar to #5, fix it on master branch, and cherry pick to ``release1`` branch. Then re-deploy. **IMPORTANT: DO NOT FIX ON release BRANCH!**.
