.. _aws-redshift-best-practice-choose-the-best-distribution-style:

Choose the best distribution style
==============================================================================
Keywords: AWS Redshift, Best practice

更多关于 distribution key 的信息请参考 :ref:`aws-redshift-working-with-data-distribution-style`

首先要知道的是 Redshift 是一个分布式系统. 数据需要根据 distribution key 来决定由哪个节点来处理这个数据.

官方文档推荐用以下几个原则来决定哪个 Column 成为 Distribution Key

1. Distribute the fact table and one dimension table on their common columns.

    Your fact table can have only one distribution key. Any tables that join on another key aren't collocated with the fact table. Choose one dimension to collocate based on how frequently it is joined and the size of the joining rows. Designate both the dimension table's primary key and the fact table's corresponding foreign key as the DISTKEY.

2. Choose the largest dimension based on the size of the filtered dataset.

    Only the rows that are used in the join need to be distributed, so consider the size of the dataset after filtering, not the size of the table.

3. Choose a column with high cardinality in the filtered result set.

    If you distribute a sales table on a date column, for example, you should probably get fairly even data distribution, unless most of your sales are seasonal. However, if you commonly use a range-restricted predicate to filter for a narrow date period, most of the filtered rows occur on a limited set of slices and the query workload is skewed.

4. Change some dimension tables to use ALL distribution.

    If a dimension table cannot be collocated with the fact table or other important joining tables, you can improve query performance significantly by distributing the entire table to all of the nodes. Using ALL distribution multiplies storage space requirements and increases load times and maintenance operations, so you should weigh all factors before choosing ALL distribution.
