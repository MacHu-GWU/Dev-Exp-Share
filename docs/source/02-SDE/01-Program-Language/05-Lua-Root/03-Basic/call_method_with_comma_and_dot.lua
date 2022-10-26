#!/usr/bin/env lua

Rectangle = {
    width = 0,
    height = 0,
}

function Rectangle:new(rect, width, height)
    rect = rect or {}
    rect.width = width or 0
    rect.height = height or 0
    return rect
end

rect1 = Rectangle:new(width=3, height=4)
print(rect1.width)