.. _compare-solution-for-checkout-additional-repo-in-cicd:

Compare Solutions for Checkout Additional Repo in CI/CD
==============================================================================

In many cases, you **need** the content of **another private repository to test the current repository**. For example, **your main repository is a public repo, but you need a secret config file from a private repository, how do you securely setup your CI/CD environment**?

Assume:

- your github organization account = ``MyORG``

Goal:

1. Your main repo’s CI/CD environment should be able to check out the private repo.
2. Anyone who has access to the public repo should not able to access anything from the private repo.


Solution 1 (Recommended)
------------------------------------------------------------------------------

Create a separate GitHub account as a Machine User, add this Machine User as a collaborator to the private repo you need to access to, and use the Machine User’s personal access token to check out the private repo in your CI/CD system.

1. Sign up a Machine User Github account, let's say, username = ``MyORG-Machine``
2. Create a personal OAuth access token (Account Settings -> Developer Settings) with full access of everything in MyORG-Machine
3. Add MyORG-Machine as a collaborator to the private, and only grant MyORG-Machine read-only access to that repo.

Code::

    # check out your main repo
    $ git clone "https://github.com/MyOrg/main-project.git"
    # check out your private repo
    $ git clone "https://${TOKEN}@github.com/MyOrg/main-project.git"

Pro:

- even the oauth access token has full access to MyORG-Machine, but MyORG-Machine's access to MyORG is limited.

Con:

- If we want to use one token to access MyORG/repo1, and another token to access MyORG/repo2, we have to create multiple users

Reference:

- Machine User: https://developer.github.com/v3/guides/managing-deploy-keys/#machine-users
- Enable Your Project to Check Out Additional Private Repositories: https://circleci.com/docs/2.0/gh-bb-integration/#enable-your-project-to-check-out-additional-private-repositories


Solution 2 (We have to trust 3rd party CICD)
------------------------------------------------------------------------------

You can grant CI/CD GitHub User Key of your GitHub account (in CircleCI, it is at ``Project settings`` -> ``Checkout SSH Keys`` -> ``Authorize with GitHub```. In other words, you grant your CI/CD system equivalent power as your GitHub Account.

Pro:

- Convenient and fast.

Con:

- If your CI/CD environment been hacked, then the hacker can do everything you can do.

Reference:

- share User Key with CircleCI: https://circleci.com/docs/2.0/gh-bb-integration/#security


Solution 3 (Too much work)
------------------------------------------------------------------------------

1. Manually create a ssh key pair, paste the public key to ``Repository Setting`` -> ``Deploy Key`` -> ``Add new Key``.
2. Use a hacky way to include the private key into CICD system, put it at ``$HOME/.ssh.id_rsa_deploy_key`` or specify that key for ``git clone`` command.

Reference:

- How to specify the private SSH-key to use when executing shell command on Git?: https://stackoverflow.com/questions/4565700/how-to-specify-the-private-ssh-key-to-use-when-executing-shell-command-on-git

Pro:

- per repo / per ssh level of grained access.

Con:

- Too much work to setup everything, especially managing and injecting the private key.

Reference:

- Generate a new SSH key and adding to your SSH agent: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key


Solution 4 (Doable)
------------------------------------------------------------------------------

Use bash script to use ssh agent to create a temp key pair in CICD system, add the public key to Github repo via Github Oauth API, and use that key pair to ssh git clone the repo.

Since you could set Personal Access Token to ``admin:public_key`` only, so you can securely use that token in your CICD system to dynamically upload public_key.

Con:

- Still much setup in your CICD scripts.

Reference:

- Create Public Key via Github API: https://developer.github.com/v3/users/keys/#create-a-public-key
