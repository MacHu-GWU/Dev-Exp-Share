#!/usr/bin/env lua

a = 1
function func1()
    a = 2
    print(string.format("inside function a = %s", a))
end
func1()
print(string.format("outside function a = %s", a))


b = 1
function func2()
    local b = 2
    print(string.format("inside function b = %s", b))
end
func2()
print(string.format("outside function b = %s", b))


local c = 1
function func3()
    c = 2
    print(string.format("inside function c = %s", c))
end
func3()
print(string.format("outside function c = %s", c))


local d = 1
function func4()
    local d = 2
    print(string.format("inside function d = %s", d))
end
func4()
print(string.format("outside function d = %s", d))
