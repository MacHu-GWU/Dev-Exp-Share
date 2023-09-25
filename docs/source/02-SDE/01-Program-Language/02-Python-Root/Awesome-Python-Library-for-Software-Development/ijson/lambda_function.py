# -*- coding: utf-8 -*-

"""
This is a solution can split large JSON file into smaller chunks (if there is a
big array node) without using much memory.

Requirements::

    ijson

**Example 1**

- Memory: 10G

if only split:

- Duration: 25s
- Max Memory Used: 540 MB

if also delete the node

- Duration: 50s
- Max Memory Used: 1037 MB

**Example 2**

- Memory: 2G

if only split:

- Duration: 25s
- Max Memory Used: 540 MB

if also delete the node

- Duration: 50s
- Max Memory Used: 1037 MB
"""

import typing as T
import json
import ijson
import dataclasses
import itertools

import boto3


s3_client = boto3.client("s3")


def split_s3_uri(uri: str) -> T.Tuple[str, str]:
    parts = uri.split("/", 3)
    bucket = parts[2]
    key = parts[3]
    return bucket, key


def get_object(uri: str):
    bucket, key = split_s3_uri(uri)
    return s3_client.get_object(
        Bucket=bucket,
        Key=key,
    )


def put_object(uri: str, body):
    bucket, key = split_s3_uri(uri)
    return s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
    )


def delete_node(
    s3uri: str,
    json_path: str,
) -> dict:
    """
    Read json file from s3, delete node at certain json path, and return the
    json data with the node deleted.

    Example::

        # example 1
        >>> input_data = {
        ...     "id": 1,
        ...     "delete": [],
        ... },
        >>> json_path = "delete"
        >>> print(output_data)
        {
            "id": 1
        },

        # example 2
        >>> input_data ={
        ...     "id": 1,
        ...     "a": {
        ...         "delete": []
        ...     },
        ... }
        >>> json_path = "a.delete"
        >>> print(output_data)
        {
            "id": 1,
            "a": {}
        }

        # example 3
        >>> input_data ={
        ...     "id": 1,
        ...     "a": {
        ...         "a_value": 2,
        ...         "b": {
        ...             "delete": [],
        ...             "b_value": 3,
        ...         },
        ...     },
        ... }
        >>> json_path = "a.b.delete"
        >>> print(output_data)
        {
            "id": 1,
            "a": {
                "a_value": 2,
                "b": {
                    "b_value": 3
                }
            }
        }
    """
    parts = json_path.split(".")
    prefix_and_key_pairs = []
    lst = list()
    for part in parts:
        prefix = ".".join(lst)
        key = part
        prefix_and_key_pairs.append((prefix, key))
        lst.append(part)

    new_data = dict()
    parent_data = new_data
    for prefix, key in prefix_and_key_pairs:
        # print(f"------ prefix = {prefix}, key = {key} ------")
        data = dict()
        with get_object(s3uri)["Body"] as f_in:
            for k, v in ijson.kvitems(f_in, prefix):
                if k != key:
                    data[k] = v
        if prefix == "":
            new_data = data
        else:
            parent_data[prefix.split(".")[-1]] = data
        parent_data = data
        # print("new_data:", new_data)

    return new_data


def take(n: int, iterable: T.Iterable):
    """
    Return first n items of the iterable as a list
    """
    return list(itertools.islice(iterable, n))


def split_json(
    s3file_input: str,
    s3dir_output: str,
    json_path: str,
    chunk_size: int,
):
    """
    :param s3file_input: the s3 uri of the input JSON file
    :param s3dir_output: the s3 uri of the output directory, it suppose to be empty
    :param json_path: the json path in dot notation to the array you want to split
    :param chunk_size: group items in the array into chunks of this size
    """
    json_path = json_path.strip(".")

    s3file_data = f"{s3dir_output}data.json"
    s3dir_arrays = f"{s3dir_output}arrays/"

    # split the big json array into many small json arrays
    with get_object(s3file_input)["Body"] as f_in:
        iterator = ijson.items(f_in, f"{json_path}.item")
        for ith in range(1, 1 + 999):
            items = take(chunk_size, iterator)
            s3path_output = f"{s3dir_arrays}{ith}.json"
            if len(items) == 0:
                break
            else:
                put_object(
                    s3path_output,
                    "\n".join([
                        json.dumps(item)
                        for item in items
                    ])
                )

    # delete the big json array node from the original json
    data = delete_node(s3uri=s3file_input, json_path=json_path)
    put_object(s3file_data, json.dumps(data))


@dataclasses.dataclass
class Request:
    """
    Lambda request event

    :param s3file_input: the s3 uri of the input JSON file
    :param s3dir_output: the s3 uri of the output directory, it suppose to be empty
    :param json_path: the json path in dot notation to the array you want to split
    :param chunk_size: group items in the array into chunks of this size
    """
    s3file_input: str
    s3dir_output: str
    json_path: str
    chunk_size: int


def lambda_handler(event, context):
    """
    Example event::

        {
            "s3file_input": "s3://807388292768-us-east-1-data/tmp/data.json",
            "s3dir_output": "s3://807388292768-us-east-1-data/tmp/output/",
            "json_path": "data.records",
            "chunk_size": 120
        }
    """
    request = Request(**event)
    split_json(
        s3file_input=request.s3file_input,
        s3dir_output=request.s3dir_output,
        json_path=request.json_path,
        chunk_size=request.chunk_size,
    )
    return {"statusCode": 200}
