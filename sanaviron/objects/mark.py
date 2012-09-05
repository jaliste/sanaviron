#!/usr/bin/python
# -*- coding: utf-8 -*-

from rectangle import Rectangle
from objects import NONE, HORIZONTAL, VERTICAL

class Mark(Rectangle):
    """This class represents a guide mark"""

    def __init__(self):
        Rectangle.__init__(self)
        self.position = 0
        self.direction = NONE

    def draw(self, context):
        position = self.position
        if self.direction == VERTICAL:
            context.move_to(self.x, position)
            context.line_to(self.x + self.width, position)
        elif self.direction == HORIZONTAL:
            context.move_to(position, self.y)
            context.line_to(position, self.y + self.height)
        context.stroke()
