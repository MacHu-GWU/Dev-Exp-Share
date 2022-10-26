.. _aws-code-artifact-advance:

CodeArtifact Advance
==============================================================================
Keywords: AWS CodeArtifact, Code Artifact


CodeArtifact Event
------------------------------------------------------------------------------
CodeArtifact 可以捕获这些 "Publish Package" 的 event. AWS Lambda 本身没有自带的 trigger 能够被 CodeArtifact 触发, 但是你可以手动配置 Event Bridge Rule 用来触发 Lambda. 这样你可以做很多高级的事情, 例如 Trigger 一个 build 来验证刚刚发布的包是否合规, 以及是否能被正确安装.

Ref:

- https://docs.aws.amazon.com/codeartifact/latest/ug/working-with-service-events.html
