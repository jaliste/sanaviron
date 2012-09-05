#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from rectangle import Rectangle
#from size import Size
from mark import Mark
from objects import HORIZONTAL, VERTICAL

class Guides(Rectangle):
    """This class represets the auxiliary guides"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = True
        #self.size = 15.0 * 8.0

        self.marks = list()

    def draw(self, context):
        ###context.save()
        self.dash = [2.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0],
                     24.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0]]
        context.set_antialias(cairo.ANTIALIAS_NONE)
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        context.set_dash(self.dash)

        for mark in self.marks:
            mark.draw(context)

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def add_mark(self, position, orientation):
        mark = Mark()
        mark.synchronize(self)
        mark.position = position
        mark.direction = orientation
        self.marks.append(mark)