# -*- coding: utf-8 -*-

from pathlib_mate import PathCls as Path
from sqlitedict import SqliteDict

cache = SqliteDict(
    Path(__file__).change(new_basename="cache.sqlite").abspath, autocommit=True)


with open(Path(__file__).change(new_basename="data.txt").abspath, "r") as f:
    content = f.read()

id_list = list()
for row in content.split("\n"):
    try:
        id_list.append(int(row))
    except:
        pass


print(id_list[-100:-1])
print(id_list[0], id_list[-1])
last_id = id_list[-1]
expect_total = (1 + last_id) * last_id / 2
print(expect_total)
print(sum(id_list))

