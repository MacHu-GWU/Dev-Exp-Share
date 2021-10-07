# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

path = str(Path(Path(__file__).parent, "datasets", "comments", "1.csv").absolute())
# df = pd.read_csv()
# print(df)

data = [
    (1, "Hello, How are you", 1, "special char: \", \' and many ...", 1),
    (1, "Hello, How are you", 1, "special char: \", \' and many ...", 1),
    (1, "Hello, How are you", 1, "special char: \", \' and many ...", 1),
    (1, "Hello, How are you", 1, "special char: \", \' and many ...", ""),
]

df = pd.DataFrame(data,columns="int_1,str_1,int_2,str_2,int_with_null".split(","))
df.to_csv(path, index=False)


# df = pd.read_csv(path)
# print(df)
