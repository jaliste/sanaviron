#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from rectangle import Rectangle
from size import Size

class Guides(Rectangle):
    """This class represets the auxiliary guides"""

    def __init__(self):
        Size.__init__(self)
        self.active = True
        self.size = 15.0 * 8.0


    def draw(self, context):
        ###context.save()
        self.dash = [2.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0],
                     24.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0]]
        context.set_antialias(cairo.ANTIALIAS_NONE)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        context.set_dash(self.dash)

        x, y = self.x, self.y

        while x <= self.x + self.width:
            context.move_to(x, self.y)
            context.line_to(x, self.y + self.height)
            x += self.size

        while y <= self.y + self.height:
            context.move_to(self.x, y)
            context.line_to(self.x + self.width, y)
            y += self.size

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()
