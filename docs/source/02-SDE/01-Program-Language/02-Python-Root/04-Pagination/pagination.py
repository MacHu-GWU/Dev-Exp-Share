# -*- coding: utf-8 -*-

"""
Implement a "return all" api based on "pagination" api
"""

n_records = 20
all_records = [
    {"id": id}
    for id in range(1, 1 + n_records)
]


def get_records(lower, upper):
    return all_records[(lower - 1):upper]


def list_records(
    limit: int = 5,
    paginator: int = None,
):
    """
    The pagination API.
    """
    if not limit:
        limit = 5
    if limit > 5:
        limit = 5

    if not paginator:
        paginator = 1

    lower = paginator
    upper = lower + limit - 1

    if upper >= n_records:
        next_paginator = None
    else:
        next_paginator = upper + 1

    return {
        "records": get_records(lower, upper),
        "next_paginator": next_paginator
    }


def test_list_records():
    # {'records': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}], 'next_paginator': 6}
    print(list_records())

    # {'records': [{'id': 1}, {'id': 2}, {'id': 3}], 'next_paginator': 4}
    print(list_records(limit=3))

    # {'records': [{'id': 6}, {'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}], 'next_paginator': 11}
    print(list_records(limit=5, paginator=6))

    # {'records': [{'id': 16}, {'id': 17}, {'id': 18}, {'id': 19}, {'id': 20}], 'next_paginator': None}
    print(list_records(limit=5, paginator=16))

    # {'records': [{'id': 18}, {'id': 19}, {'id': 20}], 'next_paginator': None}
    print(list_records(limit=5, paginator=18))


def list_all_records():
    """
    The return all API.
    """
    response_list = list()
    record_list = list()

    paginator = None
    while 1:
        response = list_records(limit=5, paginator=paginator)
        next_paginator = response["next_paginator"]
        response_list.append(response)
        if next_paginator is None:
            break
        else:
            paginator = next_paginator

    for response in response_list:
        record_list.extend(response["records"])

    return record_list


def test_list_all_records():
    print(list_all_records())


if __name__ == "__main__":
    test_list_records()
    test_list_all_records()
    pass
