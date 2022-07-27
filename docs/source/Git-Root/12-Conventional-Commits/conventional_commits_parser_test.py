# -*- coding: utf-8 -*-

import os
import pytest
from typing import List
from conventional_commits_parser import (
    tokenize, parse_commit, Commit
)


@pytest.mark.parametrize(
    "before,after",
    [
        ("a, b, c", ["a", "b", "c"]),
        ("a, b: c d e", ["a", "b", "c", "d", "e"]),
    ]
)
def test_tokenize(before: str, after: List[str]):
    assert tokenize(before) == after


@pytest.mark.parametrize(
    "msg,commit",
    [
        (
            (
                "feat, build(STORY-001): add validator\n"
                "We have done the following\n"
                "\n"
                "1. first\n"
                "2. Second\n"
                "3. Third\n"
            ),
            Commit(
                types=["feat", "build"],
                description="add validator",
                scope="STORY-001",
                breaking=None,
            )
        ),
        # No Scope
        (
            (
                "fix: be able to handle negative value\n"
                "see ``def calculate()`` function\n"
            ),
            Commit(
                types=["fix", ],
                description="be able to handle negative value",
                scope=None,
                breaking=None,
            )
        ),
        # No space after ``:``
        (
            (
                "fix:be able to handle negative value\n"
                "see ``def calculate()`` function\n"
            ),
            Commit(
                types=["fix", ],
                description="be able to handle negative value",
                scope=None,
                breaking=None,
            )
        ),
    ]
)
def test_parse_commit(msg: str, commit: Commit):
    assert parse_commit(msg) == commit


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
