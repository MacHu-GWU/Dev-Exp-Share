# -*- coding: utf-8 -*-

import sys

if __name__ == "__main__":
    lines = list()
    # 从 sys.stdin 中读取数据. 他是一个 file like object
    for line in sys.stdin.read().split("\n"):
        if "apple" in line:
            lines.append(line)
    print("\n".join(lines))
