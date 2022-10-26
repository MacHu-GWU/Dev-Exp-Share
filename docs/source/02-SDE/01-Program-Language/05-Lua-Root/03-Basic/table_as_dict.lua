#!/usr/bin/env lua

local t = {
    a = 1,
    b = 2,
}

print("--- access value from key ")
print(string.format("t[\"a\"] = %s", t["a"]))

print("--- iterate key value pair:")
for k, v in pairs(t) do
    print(string.format("key = %s, value = %s", k, v))
end

print("--- iterate key only pair:")
for k, _ in pairs(t) do
    print(string.format("key = %s", k))
end

print("--- iterate value only pair:")
for _, v in pairs(t) do
    print(string.format("value = %s", v))
end

print("--- check if table has certain key")
print(string.format("table has key \"b\": %s", t["b"] ~= nil))
print(string.format("table has key \"c\": %s", t["c"] ~= nil))

print("--- assign key value pair")
t["b"] = 20
t["c"] = 30
print(string.format("t[\"b\"] = %s, t[\"c\"] = %s", t["b"], t["c"]))

print("--- delete key value pair")
t["a"] = nil
for k, v in pairs(t) do
    print(string.format("key = %s, value = %s", k, v))
end

print("--- get number of pairs in table")
function get_table_length(t)
    local count = 0
    for _ in pairs(t) do
        count = count + 1
    end
    return count
end
print(string.format("%s", get_table_length(t)))
