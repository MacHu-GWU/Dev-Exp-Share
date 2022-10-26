#!/usr/bin/env lua

local t = {
    [1] = "a",
    [2] = "b",
    [3] = "c",
    [4] = "d",
    [5] = "e",
}

print("--- get element by index, lua index start from 1")
print(string.format("t[1] = %s", t[1]))
print(string.format("t[2] = %s", t[2]))

print("--- get the last item in the list")
print(t[#t])

print("--- get the second last item in the list")
print(t[#t - 1])

print("--- iterate a list")
for i, v in ipairs(t) do
    print(string.format("ind = %s, value = %s", i, v))
end

print("--- iterate the slice of the list")
for i, v in ipairs(t) do
    if 2 <= i and i <= 4 then
        print(string.format("ind = %s, value = %s", i, v))
    end
end

print("--- append to the end")
table.insert(t, "f")
print(t[6])

print("--- remove the last element end")
table.remove(t)
print(t[6])
print(t[5])
