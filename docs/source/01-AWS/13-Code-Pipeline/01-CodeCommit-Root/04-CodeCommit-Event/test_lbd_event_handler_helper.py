# -*- coding: utf-8 -*-

import pytest
from superjson import json
from pathlib_mate import Path

dir_sample_codecommit_events = Path.dir_here(__file__).append_parts("sample_codecommit_events")
dir_sample_codebuild_events = Path.dir_here(__file__).append_parts("sample_codebuild_events")


def print_keys(p_dir):
    keys = list()
    for p in p_dir.iterdir():
        if p.basename.endswith(".json"):
            data = json.load(f"{p}", ignore_comments=True, verbose=False)
            detail = data["detail"]
            keys.extend(list(detail))
    keys = list(set(keys))
    keys.sort()
    print(keys)


def test_print_codecommit_event_keys():
    print_keys(dir_sample_codecommit_events)


def test_print_codebuild_event_keys():
    print_keys(dir_sample_codebuild_events)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
