QuickSight
==============================================================================

Ref:

- What Is Amazon QuickSight?: https://docs.aws.amazon.com/quicksight/latest/user/welcome.html?shortFooter=true

概念:

- **Data Analysis**: 是创建和观看 Visuals 的系统.
- **Visuals**: 一个可视化图表.
- Insights: 对数据的解读.
- Sheets: set of visuals in a single page.
- **Stories**: 一连串的 Visuals 所构成的故事.
- Dashboard: 一个 Read Only snapshot of Data Analysis.
- **Spice**: 是一个 基于内存的 并行 计算引擎. https://docs.aws.amazon.com/quicksight/latest/user/welcome.html?shortFooter=true#spice
- Data Source: 一个数据源, S3, RDS, 或者用户上传的数据.
- Datasets: 一个数据源的指定部分, Dataset 同时也包含了你对 Data Source 做的所有 Preparation, 包括 transform, rename.

Data Source and Data Preparation (所支持的数据源):

- Amazon Athena
- Amazon Aurora
- Amazon Redshift
- Amazon Redshift Spectrum
- Amazon S3
- Amazon S3 Analytics
- Apache Spark 2.0 or later
- MariaDB 10.0 or later
- Microsoft SQL Server 2012 or later
- MySQL 5.1 or later
- PostgreSQL 9.3.1 or later
- Presto 0.167 or later
- Snowflake
- Teradata 14.0 or later


Visualization
------------------------------------------------------------------------------

可视化不同的数据要使用不同类型的图表, 这一点 AWS Big Specialist Certification 会考到.

Topic (重要的概念):

- Measures and Dimensions in Vxisuals: 在决定使用哪种类型的图表时, 首先要考虑你的数据里有多少个 dimension, 所谓 dimension 就是数据有多少列, 不同的列就算是 1 个 dimension. 简单来说时间序列就是 2 dimensions, Time, Value.
- Display Limits in Visuals

Graph Type:

- 各种图表类型的 AWS 官方文档: https://docs.aws.amazon.com/quicksight/latest/user/working-with-visual-types.html
- AutoGraph: 让 QuickSight 自动选择哪种图表.
- Bar Charts: Single Measure,
- Combo Charts: 混合型, 例如 Bar + Line
- Donut Charts: 甜甜圈 (环装) One Value Single Dimension
- Gauge Charts: 计量表 (体重计的图形)
- Geospatial Charts (Maps)
- Heat Maps
- KPIs: KPI指标, 一条横杠, 看达成了多少
- Line Charts
- Pie Charts
- Pivot Tables:
- Scatter Plots: 点图
- Tables as Visuals: 二维数据表本身作为 Visual
- Tree Maps: 由很多不同大小的矩形组成



