# -*- coding: utf-8 -*-

"""
The core of CI/CD on AWS CodeCommit / CodeBuild.
"""

from typing import Optional
import dataclasses

import boto3

boto_ses = boto3.session.Session()

cc_client = boto_ses.client("codecommit")
cb_client = boto_ses.client("codebuild")
s3_client = boto_ses.client("s3")


def get_commit_message(
    repo_name: str,
    commit_id: str,
    _commit_message: str = None,
) -> str:
    """
    Get a specific commit message for a commit.

    :param repo_name: CodeCommit repository name
    :param commit_id: sha1 of commit id
    :param _commit_message: the commit message body for mock
    """
    if _commit_message is None:
        res = cc_client.get_commit(
            repositoryName=repo_name,
            commitId=commit_id,
        )
        commit_message = res["commit"]["message"].strip()
    else:
        commit_message = _commit_message
    return commit_message


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
    approve_pr = "approve_pr"
    approve_rule_override = "approve_rule_override"


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

    @classmethod
    def from_detail(cls, detail: dict) -> "CodeCommitEvent":
        return cls(**detail)

    def identify_event_type(self) -> Optional[str]:
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
            return CodeCommitEventTypeEnum.comment_on_pr_created
        elif (
            self.event == "pullRequestApprovalStateChanged"
            and self.approvalStatus == "APPROVE"
        ):
            return CodeCommitEventTypeEnum.approve_pr
        elif self.event == "pullRequestApprovalRuleOverridden":
            return CodeCommitEventTypeEnum.approve_rule_override
        else:
            return None

    @property
    def event_type(self) -> str:
        if self._event_type is None:
            self._event_type = self.identify_event_type()
        return self._event_type


