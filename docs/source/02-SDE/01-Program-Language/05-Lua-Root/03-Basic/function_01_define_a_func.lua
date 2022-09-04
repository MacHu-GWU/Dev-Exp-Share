#!/usr/bin/env lua

function func(msg)
    print(string.format("msg = %s", msg))
    return "success"
end

res = func("hello alice")
print(string.format("res = %s", res))

func()
