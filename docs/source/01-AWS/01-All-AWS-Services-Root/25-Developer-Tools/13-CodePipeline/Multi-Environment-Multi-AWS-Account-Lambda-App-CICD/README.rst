::

    /projects/
    /projects/project1/...
    /projects/project2/...
    /projects/project3/...
    /bin/
    /bin/automation/...


    # Layer artifacts
    s3://bucket/projects/${project_name}/lambda/layer/000001/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000001/requirements.zip

    s3://bucket/projects/${project_name}/lambda/layer/000002/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000002/requirements.zip

    s3://bucket/projects/${project_name}/lambda/layer/000003/layer.zip
    s3://bucket/projects/${project_name}/lambda/layer/000003/requirements.zip

    # Source artifacts
    s3://bucket/projects/${project_name}/lambda/source/0.1.1/${project_name}-0.1.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.1.1/${project_name}-0.1.1.tar.gz

    s3://bucket/projects/${project_name}/lambda/source/0.2.1/${project_name}-0.2.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.2.1/${project_name}-0.2.1.tar.gz

    s3://bucket/projects/${project_name}/lambda/source/0.3.1/${project_name}-0.3.1-py3-none-any.whl
    s3://bucket/projects/${project_name}/lambda/source/0.3.1/${project_name}-0.3.1.tar.gz

    /projects/project1/...
    /projects/project2/...
    /projects/project3/...
    /bin/
    /bin/automation/...

Reference:

- `AWS DevOps Blog - Multi-branch CodePipeline strategy with event-driven architecture <https://aws.amazon.com/blogs/devops/multi-branch-codepipeline-strategy-with-event-driven-architecture/>`_