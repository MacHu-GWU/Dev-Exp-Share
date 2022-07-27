# -*- coding: utf-8 -*-

import pytest

from typing import List
import re
import json
from pathlib import Path

from codecommit_event import (
    CodeCommitEventTypeEnum as CCEventTypeEnum,
    CodeCommitEvent as CCE,
    SemanticCommitEnum,
    parse_commit_message,
)


def strip_comment_line_with_symbol(line, start):
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(re.findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part)) for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[: nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(("#", "//"))):
    """
    Strip comments from json string.
    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)
    return "\n".join(lines)


dir_codecommit_events = Path(__file__).absolute().parent / "codecommit_events"


def read_json(file: str) -> dict:
    return json.loads(strip_comments(Path(file).read_text()))


def read_cc_event(fname: str) -> CCE:
    return CCE.from_detail(
        read_json(f"{dir_codecommit_events / fname}")["detail"]
    )


class CCEventEnum:
    commit_to_master = read_cc_event("11-commit-to-master.json")
    branch_created = read_cc_event("21-branch-created.json")
    branch_updated = read_cc_event("22-branch-updated.json")
    branch_deleted = read_cc_event("23-branch-deleted.json")
    pull_request_created = read_cc_event("31-pull-request-created.json")
    pull_request_closed = read_cc_event("32-pull-request-closed.json")
    pull_request_updated = read_cc_event("33-pull-request-updated.json")
    pull_request_commit_merge_to_master = read_cc_event("34-pull-request-commit-merge-to-master.json")
    pull_request_merged = read_cc_event("35-pull-request-merged.json")
    comment_on_pull_request_specific_file = read_cc_event("41-comment-on-pull-request-specific-file.json")
    comment_on_pull_request_overall = read_cc_event("42-comment-on-pull-request-overall.json")
    reploy_to_comment = read_cc_event("43-reply-to-comment-message.json")
    approval = read_cc_event("44-approval.json")
    approval_rule_override = read_cc_event("45-approval-rule-override.json")


cc_event_list: List[dict] = [
    v for k, v in CCEventEnum.__dict__.items() if not k.startswith("_")
]


# def test_identify_event_source():
#     for message in message_list:
#         assert identify_event_source(message) == EventSourceEnum.codecommit


def test_event_type():
    assert CCEventEnum.commit_to_master.is_commit_to_branch
    assert CCEventEnum.pull_request_commit_merge_to_master.is_commit_to_branch_from_merge
    assert CCEventEnum.branch_created.is_create_branch
    assert CCEventEnum.branch_updated.is_commit_to_branch
    assert CCEventEnum.branch_deleted.is_delete_branch
    assert CCEventEnum.pull_request_created.is_pr_created
    assert CCEventEnum.pull_request_closed.is_pr_closed
    assert CCEventEnum.pull_request_updated.is_pr_update
    assert CCEventEnum.pull_request_merged.is_pr_merged
    assert CCEventEnum.comment_on_pull_request_specific_file.is_comment_on_pr_created
    assert CCEventEnum.comment_on_pull_request_overall.is_comment_on_pr_created
    assert CCEventEnum.reploy_to_comment.is_reply_to_comment
    assert CCEventEnum.approval.is_approve_pr
    assert CCEventEnum.approval_rule_override.is_approve_rule_override


def test_event_type_condition():
    pass


def test_parse_commit_message():
    assert parse_commit_message("feat") == ["feat", ]
    assert parse_commit_message("feat: this is a feature") == ["feat", ]

    assert parse_commit_message("utest, itest") == ["utest", "itest"]
    assert parse_commit_message("utest, itest: update config") == ["utest", "itest"]


#
#
# class TestCustomEnvVar:
#     def test(self):
#         custom_env_var = CustomEnvVar()
#         custom_env_var.to_env_var_override_arg()
#
#
# def test_extract_action_from_message():
#     _commit_message = "feature"
#     _codebuild_projects_data = [
#         {
#             "project_name": "my_project",
#             "is_batch_job": False,
#         }
#     ]
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.commit_to_master, _commit_message,
#                                                        _codebuild_projects_data)) != 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_created, _commit_message,
#                                                        _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_updated, _commit_message,
#                                                        _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.branch_deleted, _commit_message,
#                                                        _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_created, _commit_message,
#                                                        _codebuild_projects_data)) != 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_closed, _commit_message,
#                                                        _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_updated, _commit_message,
#                                                        _codebuild_projects_data)) != 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_commit_merge_to_master, _commit_message,
#                                                        _codebuild_projects_data)) != 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.pull_request_merged, _commit_message,
#                                                        _codebuild_projects_data)) != 0
#     assert len(
#         extract_build_job_from_codecommit_event(MessageEnum.comment_on_pull_request_specific_file, _commit_message,
#                                                 _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.comment_on_pull_request_overall, _commit_message,
#                                                        _codebuild_projects_data)) == 0
#     assert len(
#         extract_build_job_from_codecommit_event(MessageEnum.approval, _commit_message, _codebuild_projects_data)) == 0
#     assert len(extract_build_job_from_codecommit_event(MessageEnum.approval_rule_override, _commit_message,
#                                                        _codebuild_projects_data)) == 0


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
