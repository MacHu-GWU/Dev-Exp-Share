# -*- coding: utf-8 -*-

"""
A simple regex parser to parse conventional commit message.
"""

import dataclasses
import re
import string
from typing import Optional, List, Pattern

DELIMITERS = "!@#$%^&*()_+-=~`[{]}\\|;:'\",<.>/? \t\n"
CHARSET = string.ascii_letters


def tokenize(text: str) -> List[str]:
    cleaner_text = text
    for delimiter in DELIMITERS:
        cleaner_text = cleaner_text.replace(delimiter, " ")
    words = [word.strip() for word in cleaner_text.split(" ") if word.strip()]
    return words


def _get_subject_regex(_types: List[str]) -> Pattern:
    return re.compile(
        fr"^(?P<types>[\w ,]+)(?:\((?P<scope>[\w-]+)\))?(?P<breaking>!)?:[ \t]?(?P<description>.+)$"
    )


@dataclasses.dataclass
class Commit:
    """
    Data container class for conventional commits message.
    """
    types: List[str]
    description: str = None
    scope: Optional[str] = None
    breaking: Optional[str] = None


class ConventionalCommitParser:
    def __init__(self, types: List[str]):
        self.types = types
        self.subject_regex = _get_subject_regex(types)

    def extract_subject(self, msg: str) -> str:
        return msg.split("\n")[0].strip()

    def extract_commit(self, subject: str) -> Commit:
        match = self.subject_regex.match(subject)
        types = [
            word.strip()
            for word in match["types"].split(",")
            if word.strip() in self.types
        ]

        # Debug only
        # print(match)
        # print([match["types"],])
        # print([match["description"], ])
        # print([match["scope"], ])
        # print([match["breaking"], ])

        return Commit(
            types=types,
            description=match["description"],
            scope=match["scope"],
            breaking=match["breaking"],
        )


parser = ConventionalCommitParser(
    types=[
        "chore",
        "feat",
        "test",
        "utest",
        "itest",
        "build",
        "pub",
        "fix",
        "rls",
        "doc",
        "style",
        "lint",
        "ci",
        "noci",
    ]
)


def parse_commit(msg: str) -> Commit:
    subject = parser.extract_subject(msg)
    return parser.extract_commit(subject)
