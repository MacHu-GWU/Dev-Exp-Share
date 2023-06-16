#!/bin/sh
# content of long_running_script.sh
# 每 3 秒打印一次系统时间, 永不停止, 除非手动停止

while :; do
echo $(date +"%T")
sleep 3
done
