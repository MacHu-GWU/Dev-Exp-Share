# -*- coding: utf-8 -*-

"""
Keep writing 10 MB small file to current directory. up to 1GB in total.

This will increase CPU and Disk usage on EC2
"""

import math
import os
import random
import string
from datetime import datetime


class Setting:
    memory_in_mb = 500
    disk_in_mb = 3000
    executing_time_in_seconds = 3600


x_mb_per_file = int(Setting.memory_in_mb / 5)
n_file = int(Setting.disk_in_mb * 1.0 / x_mb_per_file)


def random_x_mb_text(x):
    one_kb_text = "".join([random.choice(string.ascii_lowercase) for _ in range(1000)])
    return one_kb_text * (x * 1000)


def generate_file(file_storage_dir, n_file):
    filename = "{}.txt".format(random.randint(1, n_file))
    filepath = os.path.join(file_storage_dir, filename)
    x_mb_content = random_x_mb_text(x_mb_per_file)
    with open(filepath, "wb") as f:
        f.write(x_mb_content.encode("utf-8"))


here_dir = os.path.dirname(os.path.abspath(__file__))
file_storage_dir = os.path.join(here_dir, "cpu_memory_disk_usage_test")
if not os.path.exists(file_storage_dir):
    os.mkdir(file_storage_dir)

# test how long it takes to write 500MB data
start_time = datetime.utcnow()

repeat_times_for_500mb_data = int(math.ceil(500 * 1.0 / x_mb_per_file))
for _ in range(repeat_times_for_500mb_data):
    generate_file(file_storage_dir, n_file)
end_time = datetime.utcnow()
total_seconds = (end_time - start_time).total_seconds()

# run final test
repeat_times = int((Setting.executing_time_in_seconds * 1.0 / total_seconds) * repeat_times_for_500mb_data)

msg = """
expected to consume:

- {} MB memory
- {} MB disk
- create {} random files, {} MB per file
expected to run for {} seconds
""".format(
    Setting.memory_in_mb,
    Setting.disk_in_mb,
    n_file,
    x_mb_per_file,
    Setting.executing_time_in_seconds,
)
print(msg)

start_time = datetime.utcnow()
for _ in range(repeat_times):
    generate_file(file_storage_dir, n_file)
end_time = datetime.utcnow()
total_seconds = (end_time - start_time).total_seconds()

print("total elapse {}".format(total_seconds))
