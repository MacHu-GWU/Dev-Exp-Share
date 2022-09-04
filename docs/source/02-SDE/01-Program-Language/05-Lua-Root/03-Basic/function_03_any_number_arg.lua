#!/usr/bin/env lua

-- Ref: https://www.runoob.com/lua/lua-functions.html

function func(...)
	local args = {...}
   	for _, arg in ipairs(args) do
		print(arg)
   	end
end

func("alice", "bob")
