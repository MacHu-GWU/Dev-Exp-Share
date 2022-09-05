#!/usr/bin/env lua

function add_two(arg)
    return arg.a + arg.b
end

print(add_two({a=1, b=2}))
