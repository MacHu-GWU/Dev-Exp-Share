# -*- coding: utf-8 -*-

"""
The core of CI/CD on AWS CodeCommit / CodeBuild.

This solution requires >= Python3.8 because of the ``cached_property``
Since it is only used in the AWS Lambda Function, there's no need to use
this inside of your application code.
"""

from typing import List, Optional
import dataclasses
from functools import cached_property
import boto3

boto_ses = boto3.session.Session()

cc_client = boto_ses.client("codecommit")
cb_client = boto_ses.client("codebuild")
s3_client = boto_ses.client("s3")


# ------------------------------------------------------------------------------
# Step 1.1 Declare Helper Functions
# ------------------------------------------------------------------------------
def get_commit_message(repo_name: str, commit_id: str) -> str:
    """
    Get a specific commit message for a commit.

    :param repo_name: CodeCommit repository name
    :param commit_id: sha1 of commit id
    """
    res = cc_client.get_commit(
        repositoryName=repo_name,
        commitId=commit_id,
    )
    commit_message = res["commit"]["message"].strip()
    return commit_message


# ------------------------------------------------------------------------------
# Step 1. Identify Event Source Type
# ------------------------------------------------------------------------------
class EventSourceEnum:
    codecommit = "codecommit"
    codebuild = "codebuild"


def identify_event_source(event: dict) -> str:
    """
    Identify that whether the event is from CodeCommit or CodeBuild.
    """
    if event["source"] == "aws.codecommit":
        return EventSourceEnum.codecommit
    elif event["source"] == "aws.codebuild":
        return EventSourceEnum.codebuild
    else:  # pragma: no cover
        raise NotImplementedError


# ------------------------------------------------------------------------------
# Step 2.2 Declare CodeCommit Event Data Model
# ------------------------------------------------------------------------------
class CodeCommitEventTypeEnum:
    """
    Enumerate common CodeCommit notification event type.

    It is the value of the :meth:`CodeCommitEvent.event_type` method.
    """
    commit_to_branch = "commit_to_branch"
    commit_to_branch_from_merge = "commit_to_branch_from_merge"
    create_branch = "create_branch"
    delete_branch = "delete_branch"
    pr_created = "pr_created"
    pr_closed = "pr_closed"
    pr_updated = "pr_updated"
    pr_merged = "pr_merged"
    comment_on_pr_created = "comment_on_pr_created"
    reply_to_comment = "reply_to_comment"
    approve_pr = "approve_pr"
    approve_rule_override = "approve_rule_override"
    unknown = "unknown"


@dataclasses.dataclass
class CodeCommitEvent:
    """
    Data container class to represent a CodeCommit notification event.
    """
    afterCommitId: Optional[str] = None
    approvalStatus: Optional[str] = None
    author: Optional[str] = None
    beforeCommitId: Optional[str] = None
    callerUserArn: Optional[str] = None
    commentId: Optional[str] = None
    commitId: Optional[str] = None
    creationDate: Optional[str] = None
    destinationCommit: Optional[str] = None
    destinationCommitId: Optional[str] = None
    destinationReference: Optional[str] = None
    event: Optional[str] = None
    isMerged: Optional[str] = None
    inReplyTo: Optional[str] = None
    lastModifiedDate: Optional[str] = None
    mergeOption: Optional[str] = None
    notificationBody: Optional[str] = None
    oldCommitId: Optional[str] = None
    overrideStatus: Optional[str] = None
    pullRequestId: Optional[str] = None
    pullRequestStatus: Optional[str] = None
    referenceFullName: Optional[str] = None
    referenceName: Optional[str] = None
    referenceType: Optional[str] = None
    repositoryId: Optional[str] = None
    repositoryName: Optional[str] = None
    repositoryNames: Optional[list] = None
    revisionId: Optional[str] = None
    sourceCommit: Optional[str] = None
    sourceCommitId: Optional[str] = None
    sourceReference: Optional[str] = None
    title: Optional[str] = None

    _event_type: Optional[str] = None
    _commit_message: Optional[str] = None

    @classmethod
    def from_detail(cls, detail: dict) -> "CodeCommitEvent":
        return cls(**detail)

    @cached_property
    def event_type(self) -> str:
        if self.event == "referenceUpdated":
            if self.mergeOption is None:
                return CodeCommitEventTypeEnum.commit_to_branch
            else:
                return CodeCommitEventTypeEnum.commit_to_branch_from_merge
        elif self.event == "referenceCreated":
            return CodeCommitEventTypeEnum.create_branch
        elif self.event == "referenceDeleted":
            return CodeCommitEventTypeEnum.delete_branch
        elif self.event == "pullRequestCreated":
            if (
                self.isMerged == "False"
                and self.pullRequestStatus == "Open"
            ):
                return CodeCommitEventTypeEnum.pr_created
            else:
                raise NotImplementedError
        elif (
            self.event == "pullRequestStatusChanged"
            and self.pullRequestStatus == "Closed"
        ):
            return CodeCommitEventTypeEnum.pr_closed
        elif self.event == "pullRequestSourceBranchUpdated":
            return CodeCommitEventTypeEnum.pr_updated
        elif (
            self.event == "pullRequestMergeStatusUpdated"
            and self.isMerged == "True"
            and self.pullRequestStatus == "Closed"
        ):
            return CodeCommitEventTypeEnum.pr_merged
        elif self.event == "commentOnPullRequestCreated":
            if self.inReplyTo is None:
                return CodeCommitEventTypeEnum.comment_on_pr_created
            else:
                return CodeCommitEventTypeEnum.reply_to_comment
        elif (
            self.event == "pullRequestApprovalStateChanged"
            and self.approvalStatus == "APPROVE"
        ):
            return CodeCommitEventTypeEnum.approve_pr
        elif self.event == "pullRequestApprovalRuleOverridden":
            return CodeCommitEventTypeEnum.approve_rule_override

        else:
            return CodeCommitEventTypeEnum.unknown

    @cached_property
    def repo_name(self) -> str:
        if self.repositoryName is None:
            return self.repositoryNames[0]
        else:
            return self.repositoryName

    # Event Type Condition
    @cached_property
    def is_commit_to_branch(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.commit_to_branch

    @cached_property
    def is_commit_to_branch_from_merge(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.commit_to_branch_from_merge

    @cached_property
    def is_commit(self) -> bool:
        return self.is_commit_to_branch or self.is_commit_to_branch_from_merge

    @cached_property
    def is_create_branch(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.create_branch

    @cached_property
    def is_delete_branch(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.delete_branch

    @cached_property
    def is_commit_to_branch_from_merge(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.commit_to_branch_from_merge

    @cached_property
    def is_pr_created(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.pr_created

    @cached_property
    def is_pr_closed(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.pr_closed

    @cached_property
    def is_pr_update(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.pr_updated

    @cached_property
    def is_pr_merged(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.pr_merged

    @cached_property
    def is_comment_on_pr_created(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.comment_on_pr_created

    @cached_property
    def is_reply_to_comment(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.reply_to_comment

    @cached_property
    def is_approve_pr(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.approve_pr

    @cached_property
    def is_approve_rule_override(self) -> bool:
        return self.event_type == CodeCommitEventTypeEnum.approve_rule_override

    @cached_property
    def is_pr(self) -> bool:
        return (
            self.is_pr_created
            or self.is_pr_update
            or self.is_pr_merged
            or self.is_pr_closed
        )

    @cached_property
    def is_pr_created_or_updated(self) -> bool:
        return self.is_pr_created or self.is_pr_update

    # Condition
    def assert_is_pr(self):
        if not self.is_pr:
            raise TypeError("Not a Pull Request Event")

    @cached_property
    def source_branch(self) -> str:
        if self.is_pr:
            return self.sourceReference
        elif self.is_commit:
            return self.referenceName
        else:
            raise NotImplementedError

    @cached_property
    def source_commit(self) -> str:
        if self.is_pr:
            return self.sourceCommit
        elif self.is_commit:
            return self.commitId
        else:
            raise NotImplementedError

    @cached_property
    def target_branch(self) -> str:
        if self.is_pr:
            return self.destinationReference
        else:
            raise NotImplementedError

    @cached_property
    def target_commit(self) -> str:
        if self.is_pr:
            return self.destinationCommit
        elif self.is_commit:
            return self.oldCommitId
        else:
            raise NotImplementedError

    @cached_property
    def source_commit_message(self) -> str:
        return get_commit_message(
            repo_name=self.repo_name,
            commit_id=self.source_commit,
        )

    @cached_property
    def commit_message(self) -> str:
        return self.source_commit_message

    @cached_property
    def pr_id(self) -> str:
        self.assert_is_pr()
        return self.pullRequestId

    @cached_property
    def pr_status(self) -> str:
        self.assert_is_pr()
        return self.pullRequestStatus

    @cached_property
    def pr_is_open(self) -> bool:
        return self.pr_status == "Open"

    @cached_property
    def pr_is_merged(self) -> bool:
        self.assert_is_pr()
        return self.isMerged == "False"

    # identify branch
    @cached_property
    def source_is_main_branch(self):
        return is_main_branch(self.source_branch)

    @cached_property
    def source_is_develop_branch(self):
        return is_develop_branch(self.source_branch)

    @cached_property
    def source_is_feature_branch(self):
        return is_feature_branch(self.source_branch)

    @cached_property
    def source_is_release_branch(self):
        return is_release_branch(self.source_branch)

    @cached_property
    def source_is_hotfix_branch(self):
        return is_hotfix_branch(self.source_branch)

    @cached_property
    def is_main_branch(self):
        return self.source_is_main_branch

    @cached_property
    def is_develop_branch(self):
        return self.source_is_develop_branch

    @cached_property
    def is_feature_branch(self):
        return self.source_is_feature_branch

    @cached_property
    def is_release_branch(self):
        return self.source_is_release_branch

    @cached_property
    def is_hotfix_branch(self):
        return self.source_is_hotfix_branch

    @cached_property
    def target_is_main_branch(self):
        return is_main_branch(self.target_branch)

    @cached_property
    def target_is_develop_branch(self):
        return is_develop_branch(self.target_branch)

    @cached_property
    def target_is_feature_branch(self):
        return is_feature_branch(self.target_branch)

    @cached_property
    def target_is_release_branch(self):
        return is_release_branch(self.target_branch)

    @cached_property
    def target_is_hotfix_branch(self):
        return is_hotfix_branch(self.target_branch)

    # identify commit message
    @cached_property
    def is_feat_commit(self) -> bool:
        return SemanticCommitEnum.feat in parse_commit_message(self.commit_message)

    @cached_property
    def is_utest_commit(self) -> bool:
        return SemanticCommitEnum.itest in parse_commit_message(self.commit_message)

    @cached_property
    def is_itest_commit(self) -> bool:
        return SemanticCommitEnum.utest in parse_commit_message(self.commit_message)

    @cached_property
    def is_ltest_commit(self) -> bool:
        return SemanticCommitEnum.ltest in parse_commit_message(self.commit_message)

    @cached_property
    def is_test_commit(self) -> bool:
        acts = parse_commit_message(self.commit_message)
        return (
            SemanticCommitEnum.utest in acts
            or SemanticCommitEnum.itest in acts
            or SemanticCommitEnum.ltest in acts
        )

    @cached_property
    def is_ltest_commit(self) -> bool:
        return SemanticCommitEnum.ltest in parse_commit_message(self.commit_message)


MAIN_BRANCH = ["master", "main"]


def is_main_branch(name: str) -> bool:
    return name in MAIN_BRANCH


def is_develop_branch(name: str) -> bool:
    return (
        name.startswith("dev/")
        or name.startswith("develop/")
        or name == "dev"
        or name == "develop"
    )


def is_feature_branch(name: str) -> bool:
    return (
        name.startswith("feat/")
        or name.startswith("feature/")
        or name == "feat"
        or name == "feature"
    )


def is_release_branch(name: str) -> bool:
    return (
        name.startswith("rls/")
        or name.startswith("release/")
        or name == "rls"
        or name == "release"
    )


def is_hotfix_branch(name: str) -> bool:
    return (
        name.startswith("fix/")
        or name.startswith("hotfix/")
        or name == "fix"
        or name == "hotfix"
    )


# ------------------------------------------------------------------------------
# Semantic Commit
# ------------------------------------------------------------------------------
class SemanticCommitEnum:
    """
    Semantic commit message can help CI to determine what you want to do.
    It is a good way to allow developer controls the CI behavior with small
    effort.
    """
    chore = "chore"  # house cleaning, do nothing
    feat = "feat"  # feature, message can be automatically picked up in description
    build = "build"  # build artifacts
    pub = "pub"  # publish artifacts
    test = "test"  # run all test
    utest = "utest"  # run unit test
    itest = "itest"  # run integration test
    ltest = "ltest"  # run load test
    rls = "rls"  # release
    fix = "fix"  # fix something


valid_commit_action_list = [
    v
    for k, v in SemanticCommitEnum.__dict__.items()
    if not k.startswith("_")
]
valid_commit_action_set = set(valid_commit_action_list)


def _parse_commit_message(msg: str) -> List[str]:
    if msg.strip().lower() in valid_commit_action_set:
        return [msg.strip().lower(), ]

    words = [
        word.strip().lower()
        for word in msg.split(":")[0].split(",")
        if word.strip()
    ]
    return [word for word in words if word in valid_commit_action_set]


def parse_commit_message(msg: str) -> List[str]:
    try:
        return _parse_commit_message(msg)
    except:
        return []
