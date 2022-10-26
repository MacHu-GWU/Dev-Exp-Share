#!/usr/bin/env lua

s = "a"
print(string.format("s = %s", s))
s = "b" .. s
print(string.format("s = %s", s))
s = "d" .. "c" .. s
print(string.format("s = %s", s))
s = "e"..s
print(string.format("s = %s", s))
