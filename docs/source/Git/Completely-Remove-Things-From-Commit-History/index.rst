Completely Remove Things From Commit History
============================================

Why? You accidentally checked in:

- Large Binary File, for example ``.zip`` file.
- Sensitive Credential Data.

Solution:

1. Remove specific file from commit history.
2. Remove entire commit.

<1> is better than <2>, because you may remove good files with <2>.


Remove File
-----------

.. code-block:: bash

    git filter-branch --force --index-filter \
      'git rm --cached --ignore-unmatch <PATH-to-File-to-Delete.zip>' \
      --prune-empty --tag-name-filter cat -- --all

    git push origin --force --all

``PATH-to-File-to-Delete`` is the relative path. For example::

    repo-dir
    |-- folder1
        |-- credential.txt

Then ``PATH-to-File-to-Delete`` = ``folder1/credential.txt``

Reference:

- Using filter-branch: https://help.github.com/en/articles/removing-sensitive-data-from-a-repository#using-filter-branch