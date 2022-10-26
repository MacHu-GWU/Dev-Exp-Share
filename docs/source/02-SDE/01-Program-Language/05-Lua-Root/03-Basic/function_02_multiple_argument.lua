#!/usr/bin/env lua

function func(msg1, msg2)
	print(string.format("msg1 = %s", msg1))
	print(string.format("msg2 = %s", msg2))
	return "success"
end

func("hello alice", "hello bob")
