#!/bin/bash

NOW="2017-01-03 08:30:00"
NOW_DATE=$(python -c "print('${NOW}'[:10])") # 由于我们需要使用 ${} 将变量值传递给 Python, 所以我们需要使用双引号 " 作为最外层的标记.
echo $NOW_DATE