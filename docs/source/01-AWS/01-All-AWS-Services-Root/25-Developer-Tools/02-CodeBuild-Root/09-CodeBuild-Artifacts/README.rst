CodeBuild Artifacts
==============================================================================
Example1:

    Artifact Settings:

    - Name: "Enable semantic versioning"
    - Path (optional): NA
    - Namespace type: None

    Buildspec::

        artifacts:
          files:
            - data.json
          name: my_artifacts-$(date +%Y-%m-%d-%H-%M-%S)

    Final Artifacts: ``s3://bucket/my_artifacts-2023-01-01-08-30-00/data.json``

Example2:

    Artifact Settings:

    - Name: "Enable semantic versioning"
    - Path (optional): ``projects/learn_codepipeline/``
    - Namespace type: None

    Buildspec::

        artifacts:
          files:
            - data.json
          name: my_artifacts-$(date +%Y-%m-%d-%H-%M-%S)

    Final Artifacts: ``s3://bucket/projects/learn_codepipeline/my_artifacts-2023-01-01-08-30-00/data.json``

Example3:

    Artifact Settings:

    - Name: "Enable semantic versioning"
    - Path (optional): ``projects/learn_codepipeline/``
    - Namespace type: Build ID

    Buildspec::

        artifacts:
          files:
            - data.json
          name: my_artifacts-$(date +%Y-%m-%d-%H-%M-%S)

    Final Artifacts: ``s3://bucket/projects/learn_codepipeline/74ec4684-b0be-4ec5-afba-4161dd11baa8/my_artifacts-2023-01-01-08-30-00/data.json``


Example4:

    Concent of ``print_version.py``::

        __version__ = "0.1.1"
        print(__version__)

    Artifact Settings:

    - Name: "Enable semantic versioning"
    - Path (optional): ``projects/learn_codepipeline/``
    - Namespace type: Build ID

    Buildspec::

        artifacts:
          files:
            - data.json
          name: my_artifacts-$(date +%Y-%m-%d-%H-%M-%S)-$(python print_version.py)

    Final Artifacts: ``s3://bucket/projects/learn_codepipeline/74ec4684-b0be-4ec5-afba-4161dd11baa8/my_artifacts-2023-01-01-08-30-00-0.1.1/data.json``

