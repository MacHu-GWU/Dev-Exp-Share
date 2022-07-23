# -*- coding: utf-8 -*-

from typing import List
import pytest
from superjson import json
from pathlib_mate import Path

from aws_data_lab_open_source_infra.lbd.ci_bot_handler import (
    EventSourceEnum,
    identify_event_source,
    CodeCommitEventTypeEnum,
    CodeCommitEvent,
    CustomEnvVar,
    extract_build_job_from_codecommit_event,
)

dir_sample_events = Path.dir_here(__file__).append_parts("sample_codecommit_events")


def read_data(filename: str) -> dict:
    return json.loads(
        Path(dir_sample_events, filename).read_text(),
        ignore_comments=True,
    )


class MessageEnum:
    commit_to_master = read_data("11-commit-to-master.json")
    branch_created = read_data("21-branch-created.json")
    branch_updated = read_data("22-branch-updated.json")
    branch_deleted = read_data("23-branch-deleted.json")
    pull_request_created = read_data("31-pull-request-created.json")
    pull_request_closed = read_data("32-pull-request-closed.json")
    pull_request_updated = read_data("33-pull-request-updated.json")
    pull_request_commit_merge_to_master = read_data(
        "34-pull-request-commit-merge-to-master.json"
    )
    pull_request_merged = read_data("35-pull-request-merged.json")
    comment_on_pull_request_specific_file = read_data(
        "41-comment-on-pull-request-specific-file.json"
    )
    comment_on_pull_request_overall = read_data(
        "42-comment-on-pull-request-overall.json"
    )
    approval = read_data("43-approval.json")
    approval_rule_override = read_data("44-approval-rule-override.json")


message_list: List[dict] = [
    v for k, v in MessageEnum.__dict__.items() if not k.startswith("_")
]


def test_identify_event_source():
    for message in message_list:
        assert identify_event_source(message) == EventSourceEnum.codecommit


def test_parse_event_type():
    assert (
        CodeCommitEvent.from_detail(MessageEnum.commit_to_master["detail"]).event_type
        == CodeCommitEventTypeEnum.commit_to_branch
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.branch_created["detail"]).event_type
        == CodeCommitEventTypeEnum.create_branch
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.branch_updated["detail"]).event_type
        == CodeCommitEventTypeEnum.commit_to_branch
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.branch_deleted["detail"]).event_type
        == CodeCommitEventTypeEnum.delete_branch
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.pull_request_created["detail"]).event_type
        == CodeCommitEventTypeEnum.pr_created
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.pull_request_closed["detail"]).event_type
        == CodeCommitEventTypeEnum.pr_closed
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.pull_request_updated["detail"]).event_type
        == CodeCommitEventTypeEnum.pr_updated
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.pull_request_commit_merge_to_master["detail"]).event_type
        == CodeCommitEventTypeEnum.commit_to_branch_from_merge
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.pull_request_merged["detail"]).event_type
        == CodeCommitEventTypeEnum.pr_merged
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.comment_on_pull_request_specific_file["detail"]).event_type
        == CodeCommitEventTypeEnum.comment_on_pr_created
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.comment_on_pull_request_overall["detail"]).event_type
        == CodeCommitEventTypeEnum.comment_on_pr_created
    )
    assert (
        CodeCommitEvent.from_detail(MessageEnum.approval["detail"]).event_type
        == CodeCommitEventTypeEnum.approve_pr
    )


class TestCustomEnvVar:
    def test(self):
        custom_env_var = CustomEnvVar()
        custom_env_var.to_env_var_override_arg()


def test_extract_action_from_message():
    _commit_message = "feature"
    _codebuild_projects_data = [
        {
            "project_name": "my_project",
            "is_batch_job": False,
        }
    ]
    assert len(extract_build_job_from_codecommit_event(MessageEnum.commit_to_master, _commit_message,
                                                       _codebuild_projects_data)) != 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_created, _commit_message,
                                                       _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_updated, _commit_message,
                                                       _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_deleted, _commit_message,
                                                       _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_created, _commit_message,
                                                       _codebuild_projects_data)) != 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_closed, _commit_message,
                                                       _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_updated, _commit_message,
                                                       _codebuild_projects_data)) != 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_commit_merge_to_master, _commit_message,
                                                       _codebuild_projects_data)) != 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_merged, _commit_message,
                                                       _codebuild_projects_data)) != 0
    assert len(
        extract_build_job_from_codecommit_event(MessageEnum.comment_on_pull_request_specific_file, _commit_message,
                                                _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.comment_on_pull_request_overall, _commit_message,
                                                       _codebuild_projects_data)) == 0
    assert len(
        extract_build_job_from_codecommit_event(MessageEnum.approval, _commit_message, _codebuild_projects_data)) == 0
    assert len(extract_build_job_from_codecommit_event(MessageEnum.approval_rule_override, _commit_message,
                                                       _codebuild_projects_data)) == 0


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
