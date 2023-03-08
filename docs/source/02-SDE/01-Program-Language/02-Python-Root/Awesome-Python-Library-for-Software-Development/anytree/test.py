from anytree import (
    Node,
    RenderTree,
    ContStyle,
    AsciiStyle,
    ContRoundStyle,
    DoubleStyle,
)

root = Node("root")

ou_ml = Node("ou_ml", parent=root)
ml_dev = Node("ml_dev", parent=ou_ml)
ml_staging = Node("ml_staging", parent=ou_ml)
ml_prod = Node("ml_prod", parent=ou_ml)

ou_app = Node("ou_app", parent=root)
app_dev = Node("app_dev", parent=ou_app)
app_staging = Node("app_staging", parent=ou_app)
app_prod = Node("app_prod", parent=ou_app)

for row in RenderTree(root):
    print(row.node)

# print(RenderTree(root))
# print(RenderTree(root, ContStyle()))
# print(RenderTree(root, ContRoundStyle()))
# print(RenderTree(root, AsciiStyle()))
# print(RenderTree(root, DoubleStyle()))
