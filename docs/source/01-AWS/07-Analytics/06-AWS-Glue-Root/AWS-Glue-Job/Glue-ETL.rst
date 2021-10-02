Glue Crawler 在检测到数据的 Schema 跟 Catalog 中定义的的不一样时候, 你可以选择三种更新策略:

1. Update Catalog.
2. 只有在检测到新增的 Column 的时候才 Update Catalog. 已有的 Column 的 Data Type 变化了也不更新 Catalog.
3. 完全忽略 Schema Change.

首先我们要了解 Glue Crawler 在面对同一个文件夹中, Schema 不一致的情况时, 行为是怎样的.

考虑如下 dataset, 在一个 S3 folder 内一共 3 个文件, 正确的 Schema 是 acc: int, balance: int. 但是 2.json 里有一条错误数据.

1.json::

    {"acc": 0, "balance": 0}
    {"acc": 1, "balance": 0}
    {"acc": 2, "balance": 0}
    {"acc": 3, "balance": 0}
    {"acc": 4, "balance": 0}
    {"acc": 5, "balance": 0}
    {"acc": 6, "balance": 0}
    {"acc": 7, "balance": 0}
    {"acc": 8, "balance": 0}
    {"acc": 9, "balance": 0}

2.json::

    {"acc": 10, "balance": 0}
    {"acc": 11, "balance": 0}
    {"acc": 12, "balance": 0}
    {"acc": 13, "balance": 0}
    {"acc": 14, "balance": 0}
    {"acc": 15, "balance": 0}
    {"acc": 16, "balance": 0}
    {"acc": 17, "balance": "wrong-value"}
    {"acc": 18, "balance": 0}
    {"acc": 19, "balance": 0}

3.json::

    {"acc": 20, "balance": 0}
    {"acc": 21, "balance": 0}
    {"acc": 22, "balance": 0}
    {"acc": 23, "balance": 0}
    {"acc": 24, "balance": 0}
    {"acc": 25, "balance": 0}
    {"acc": 26, "balance": 0}
    {"acc": 27, "balance": 0}
    {"acc": 28, "balance": 0}
    {"acc": 29, "balance": 0}

如果 1, 2, 3.json 都在文件夹下, crawler 会推断 balance 是 str 而不是 int, 即使在 json 中完全不可能存在 csv 中会有的 int / string 难以判断的问题.

如果第一次 run crawler 的时候只有 1, 3.json, crawler 会得到正确的 schema. 但是添加 2.json 后重新 run crawler, 那么, 如果你允许 Update Catalog, 那么 schema 会变为 balance: str. 如果你选择只允许 add new column, 那么依然是 int.

不过, 即使在 Catalog 的 schema 是 int 的前提下, 你用 glueContext.create_dynamic_frame_from_options 或是 glueContext.create_dynamic_frame_from_catalog 得到的数据依然是 int.

在某打工

- Schema 相同, 但是数据格式不同的文件被 Upload 到同一个 S3 Folder 里, 有 csv, json, excel.
- 这些数据文件中偶尔会出现 Schema 的错误, 例如某个 Column 是 Int, 但是数值却是一个 String.