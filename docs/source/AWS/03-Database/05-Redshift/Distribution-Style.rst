Distribution Style
==============================================================================

Reference: https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html

- Auto: With AUTO distribution, Amazon Redshift assigns an optimal distribution style based on the size of the table data. For example, Amazon Redshift initially assigns ALL distribution to a small table, then changes to EVEN distribution when the table grows larger. When a table is changed from ALL to EVEN distribution, storage utilization might change slightly. The change in distribution occurs in the background, in a few seconds. Amazon Redshift never changes the distribution style from EVEN to ALL. To view the distribution style applied to a table, query the PG_CLASS_INFO system catalog view. For more information, see Viewing Distribution Styles. If you don't specify a distribution style with the CREATE TABLE statement, Amazon Redshift applies AUTO distribution.
- Even: The leader node distributes the rows across the slices in a round-robin fashion, regardless of the values in any particular column. EVEN distribution is appropriate when a table does not participate in joins or when there is not a clear choice between KEY distribution and ALL distribution.
- Key: The rows are distributed according to the values in one column. The leader node places matching values on the same node slice. If you distribute a pair of tables on the joining keys, the leader node collocates the rows on the slices according to the values in the joining columns so that matching values from the common columns are physically stored together.
- All: A copy of the entire table is distributed to every node. Where EVEN distribution or KEY distribution place only a portion of a table's rows on each node, ALL distribution ensures that every row is collocated for every join that the table participates in.

中文版

- Auto: 当表很小时, 使用 ALL, 当表变大后, 使用 Even, 然后就再也不变了.
- Even: 用轮询的方式, 将数据平均的分配到 Node 上. 当使用 Key 和 All 的好处不是很明显时使用这一模式.
- Key: 使用一个 Column 作为 Partition Key. 当该表比较大, 而有一列经常是 Primary Key 并且变化非常大, 还经常需要做 Join 时, 使用这一模式.
- All: 每个 Node 的第一个 Slice 上都有该 Table 的一个副本. 常用于很小的表, 并且频繁被 Join 的表. 比如 Tag(tag_id, tag_name). 总共也不过 1000 个 Tag, 而 TagName 很长, 在其他表中你只储存 Id, 而你的查询结果中要使用 TagName.

Example: https://docs.aws.amazon.com/redshift/latest/dg/c_Distribution_examples.html