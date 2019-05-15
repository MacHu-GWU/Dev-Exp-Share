Compare Solutions for Checkout Additional Repo in CI/CD
==============================================================================

Assume:

- your github organization account = MyORG

Goal:

1. Securely Checkout source code of additional repository with proper access (Read only preferred).
2. The access method our CICD used should not be able to read / write other repository.


Solution 1 (Recommended)
------------------------------------------------------------------------------

1. sign up a github account for Enquizit, let's say, username = MyORG-Machine
2. create an personal oauth access token (Account Settings -> Developer Settings) with full access of everything in MyORG-Machine
3. MyORG-Machine as collaborator to the repo we need machine user access, and only grant MyORG-Machine read only access to that repo.

Pro:

- even the oauth access token has full access to MyORG-Machine, but MyORG-Machine's access to MyORG is limited.

Con:

- If we want to use one token to access MyORG/repo1, and another token to access MyORG/repo2, we have to create multiple users

Reference:

- Machine User: https://developer.github.com/v3/guides/managing-deploy-keys/#machine-users
- nable Your Project to Check Out Additional Private Repositories: https://circleci.com/docs/2.0/gh-bb-integration/#enable-your-project-to-check-out-additional-private-repositories


Solution 2 (We have to trust 3rd party CICD)
------------------------------------------------------------------------------

1. Grant CICD GitHub User Key (in CircleCI, it is at ``project settings`` -> ``Checkout SSH Keys`` -> ``Authorize with GitHub```.

Pro:

- convenient and fast.

Con:

- It grants CICD system admin access to your GitHub Repo.

Reference:

- share User Key with CircleCI: https://circleci.com/docs/2.0/gh-bb-integration/#security


Solution 3 (Too much work)
------------------------------------------------------------------------------

1. manually create a ssh key pair, paste the public key to ``Repository Setting`` -> ``Deploy Key`` -> ``Add new Key``.
2. use a hacky way to include the private key into CICD system, put it at ``$HOME/.ssh.id_rsa_deploy_key`` or specify that key for ``git clone`` command.

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

