import pandas as pd

data = [
    # (1, {"key": "value1"}, [1, 2, 3], {}),
    # (2, {"key": "value2"}, [1, 2, 3], {}),
    (1, True),
    (2, False),
]
df = pd.DataFrame(data, columns=["id", "data"])
df.to_csv("test.csv", index=False)
