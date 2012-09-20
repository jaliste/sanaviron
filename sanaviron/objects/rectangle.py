#!/usr/bin/python
# -*- coding: utf-8 -*-

from position import Position
from size import Size


class Rectangle(Position, Size):
    """This class represents a rectangle"""

    def __init__(self):
        Position.__init__(self)
        Size.__init__(self)

    def get_xxx(self):
        return Position.get_xxx(self) + Size.get_xxx(self)

    def synchronize(self, rectangle):
        self.x = rectangle.x
        self.y = rectangle.y
        self.width =  rectangle.width
        self.height = rectangle.height