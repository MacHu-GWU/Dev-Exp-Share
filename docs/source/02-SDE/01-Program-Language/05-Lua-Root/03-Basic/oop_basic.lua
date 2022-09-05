#!/usr/bin/env lua

local Rectangle = {
    width = 0,
    height = 0,
}

function Rectangle:new(arg)
    rect = {}
    setmetatable(rect, self)
    self.__index = self
    rect.width = arg.width or 0
    rect.height = arg.height or 0
    return rect
end

function Rectangle:area()
    return self.width * self.height
end

rect1 = Rectangle:new({width=3, height=4})
print(rect1.width)
print(rect1:area())
