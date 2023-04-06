Monorepo CICD with CodeBuild
==============================================================================

有两种 Build 的类型.

1. Build Type: 根据 trigger, 从当前的 branch / commit 处 pull 代码, 并基于此进行部署.
2. Deploy Type: 根据 bom (build of material) 文件里的定义, 从 git tag 处 pull 代码并进行部署.

这两个