# -*- coding: utf-8 -*-

import os

here = os.path.dirname(os.path.abspath(__file__))

file_size_in_kb = 5 * 1000 # 5 MB

line = "this is a very long message"

n_character = file_size_in_kb * 1000
n_lines = n_character // (len(line) + 1)
text = "\n".join([line,]*n_lines)

with open(os.path.join(here, "big-file.txt"), "wb") as f:
    f.write(text.encode("utf-8"))
