# -*- coding: utf-8 -*-

import attr
import cottonformation as cf
from cottonformation.res import codecommit, codebuild


@attr.s
class Stack(cf.Stack):
    project_name: str = attr.ib()
    stage: str = attr.ib()

    def mk_rg1(self):
        self.rg1 = cf.ResourceGroup("RG1")

        self.code_repo = codecommit.Repository(
            "CodeCommitRepo",
            rp_RepositoryName="my_repo",
            p_RepositoryDescription="",
        )

        self.code_build = codebuild.Project(
            "CodeBuildProject",
            rp_Source="",
        )
