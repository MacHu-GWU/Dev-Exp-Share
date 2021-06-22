# -*- coding: utf-8 -*-

import boto3
import random
import time
import itertools

def grouper_list(l, n):
    """Evenly divide list into fixed-length piece, no filled value if chunk
    size smaller than fixed-length.
    Example::
        >>> list(grouper_list(range(10), n=3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    **中文文档**
    将一个列表按照尺寸n, 依次打包输出, 有多少输出多少, 并不强制填充包的大小到n。
    下列实现是按照性能从高到低进行排列的:
    - 方法1: 建立一个counter, 在向chunk中添加元素时, 同时将counter与n比较, 如果一致
      则yield。然后在最后将剩余的item视情况yield。
    - 方法2: 建立一个list, 每次添加一个元素, 并检查size。
    - 方法3: 调用grouper()函数, 然后对里面的None元素进行清理。
    """
    chunk = list()
    counter = 0
    for item in l:
        counter += 1
        chunk.append(item)
        if counter == n:
            yield chunk
            chunk = list()
            counter = 0
    if len(chunk) > 0:
        yield chunk


aws_profile = "eq_sanhe"

ses = boto3.session.Session(profile_name=aws_profile)

# sqs = ses.client("sqs")
sqs = boto3.resource('sqs')

q_url = "https://sqs.us-east-1.amazonaws.com/110330507156/sql-q.fifo"
q = sqs.Queue(q_url)

n_message = 1000

iterator = range(1, n_message+1)

n_message_per_send = 10 # aws sqs limit
for l in grouper_list(iterator, n_message_per_send):
    entries = list()
    for i in l:
        message = {
            "Id": f"{i}",
            "MessageBody": f"message {i}",
            "MessageDeduplicationId": f"{i}",
            "MessageGroupId": "root",
        }
        entries.append(message)
    print(f"send message: {l}")
    q.send_messages(Entries=entries)
    time.sleep(30)
    # print(list(itertools.islice(iterator, 10)))


# q.send_messages(
#     Entries=
# )

