#!/bin/bash
#
#doitlive speed: 3

export MY_VAR1="Alice" && export MY_VAR2="Bob" && export MY_VAR3="Cathy"

#doitlive prompt: {user} is at {cwd} $

echo $MY_VAR1
echo $MY_VAR2
echo $MY_VAR3


```python
list = [2, 4, 6, 8]
sum = 0
for num in list:
    sum = sum + num

print("The sum is: {sum}".format(sum=sum))
```
