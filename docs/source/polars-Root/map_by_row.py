import attr
import polars as pl

@attr.s
class Point:
    x: int = attr.ib()
    y: int = attr.ib()

df = pl.DataFrame(
    [[1, 2], [3, 4]],
    columns=["x", "y"],
)

df = df.select([
    pl.col("x"),
    pl.col("y"),
    pl.struct([
        "x",
        "y",
    ]).apply(
        lambda cols: Point(x=cols["x"], y=cols["y"])
    ).alias(f"point")
])

def func(row: dict) -> Point:
    return Point(x=row["x"], y=row["y"])

print(df)
print(df.to_dicts())