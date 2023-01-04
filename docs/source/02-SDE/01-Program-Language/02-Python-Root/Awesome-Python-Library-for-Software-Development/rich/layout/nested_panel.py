import shutil
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console

console = Console(height=30)

layout = Layout()

# layout.split_row(
#     Layout(Panel("col1", title="begin col1", subtitle="end col1"), name="col1"),
#     Layout(Panel("col2"), name="col2"),
# )
# layout["col2"].ratio = 2

# layout["col2"].split_column(
layout.split_column(
    Layout(
        Panel.fit(
            "\n".join([
                "col21 - line1",
                "col21 - line2 - 038a9a2fb977471fe1d7bb5f6794c400038a9a2fb977471fe1d7bb5f6794c400038a9a2fb977471fe1d7bb5f6794c400038a9a2fb977471fe1d7bb5f6794c400",
                "col21 - line3 - c36293aa1bbed35f7553d084f974dcc2c36293aa1bbed35f7553d084f974dcc2c36293aa1bbed35f7553d084f974dcc2c36293aa1bbed35f7553d084f974dcc2",
                "col21 - line4 - a1938eae1bcb5e814c79d3b0920ca021a1938eae1bcb5e814c79d3b0920ca021a1938eae1bcb5e814c79d3b0920ca021a1938eae1bcb5e814c79d3b0920ca021",
                "col21 - line5 - 6faaeae43815dedb9784ac8b9cd5d6ef6faaeae43815dedb9784ac8b9cd5d6ef6faaeae43815dedb9784ac8b9cd5d6ef6faaeae43815dedb9784ac8b9cd5d6ef",
                "col21 - line6 - 8553a15eb7ca5d081ba965fa5c6d72888553a15eb7ca5d081ba965fa5c6d72888553a15eb7ca5d081ba965fa5c6d72888553a15eb7ca5d081ba965fa5c6d7288",
            ]
            ),
            title="begin col21",
            subtitle="end col21",
        ),
        name="col21",
    ),
    Layout(Panel.fit("col22", title="begin col22", subtitle="end col22"), name="col22"),
    Layout(Panel.fit("col23", title="begin col23", subtitle="end col23"), name="col23"),
)

# layout["col2"]["col21"].ratio = 2

# layout["row1"].split_row(
#     Layout(Panel("row11"), name="row11"),
#     Layout(Panel("row12 fc787e73a8a6f0e022fe11566fe3f106 fc787e73a8a6f0e022fe11566fe3f106 fc787e73a8a6f0e022fe11566fe3f106"), name="row12"),
# )
#
# layout["row2"].split_row(
#     Layout(Panel("row21"), name="row21"),
#     Layout(Panel("row22 fc787e73a8a6f0e022fe11566fe3f106 fc787e73a8a6f0e022fe11566fe3f106 fc787e73a8a6f0e022fe11566fe3f106"), name="row22"),
# )

# print(layout.tree)

console.print(layout)