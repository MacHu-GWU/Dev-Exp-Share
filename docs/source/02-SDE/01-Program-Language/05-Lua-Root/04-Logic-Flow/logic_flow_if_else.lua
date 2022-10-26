#!/usr/bin/env lua

-- local value = 45
-- local value = 65
local value = 85

if value <= 50 then
    print(string.format("%d <= 50", value))
elseif value <= 70 then
    print(string.format("50 < %d <= 70", value))
else
    print(string.format("%d > 100", value))
end