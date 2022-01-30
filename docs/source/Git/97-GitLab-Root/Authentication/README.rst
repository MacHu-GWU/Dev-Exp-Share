
https://<my-user-id>:<my-pat>@gitlab.com/<my-account>/<my-project-name>
https://gitlab-ci-token:[MASKED]@gitlab.com/gitlab-examples/ci-debug-trace.git

GL_TOKEN="abcde-U-fgh1234abcdefg"
GL_USER="MacHu-GWU"
GL_REPO="gitlab-test"
git clone "https://oauth2:${GL_TOKEN}@gitlab.com/${GL_USER}/${GL_REPO}.git"

git clone https://oauth2:@gitlab.com/MacHu-GWU/gitlab-test.git
git clone "https://oauth2:${GL_TOKEN}@gitlab.com/MacHu-GWU/gitlab-test.git"
