#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from rectangle import Rectangle
from point import Point
from math import pi

class Control(Rectangle):
    """This class represents a control point"""

    def __init__(self):
        Rectangle.__init__(self)
        self.offset = Point()
        self.size = 10.0
        self.limbus = False

    def draw(self, context):
        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        self.width = self.size / 2.0 / context.get_matrix()[0]
        self.height = self.size / 2.0 / context.get_matrix()[0]
        dash = list()
        context.set_dash(dash)
        context.set_line_width(1.0 / context.get_matrix()[0])

        if self.limbus:
            context.set_source_rgba(1.0, 0.5, 0.5, 1.0)
            context.arc(self.x, self.y, 3 / context.get_matrix()[0], 0, 2.0 * pi)
        else:
            context.set_source_rgba(0.3, 1.0, 0.3, 1.0)
            context.rectangle(self.x - self.width / 2.0, self.y - self.height / 2.0, self.width, self.height)

        context.fill_preserve()

        if self.limbus:
            context.set_source_rgba(0.25, 0.0, 0.0, 0.5)
        else:
            context.set_source_rgba(0.0, 0.25, 0.0, 0.5)

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def at_position(self, x, y):
        return x >= (self.x - self.size / 2.0) and x <= (self.x + self.size) and\
               y >= (self.y - self.size / 2.0) and y <= (self.y + self.size)
