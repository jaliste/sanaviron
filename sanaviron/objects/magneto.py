#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk.gdk

from point import Point
from objects import NONE, HORIZONTAL, VERTICAL

class Magneto(Point):
    """This class represents a object magnetic line"""

    __name__ = "Magneto"

    def __init__(self):
        Point.__init__(self)
        self.orientation = NONE

    def draw(self, context):
        dash = [2.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0],
                24.0 / context.get_matrix()[0], 4.0 / context.get_matrix()[0]]
        context.set_line_width(1.0 / context.get_matrix()[0])
        #context.set_dash(dash)

        context.move_to(0, self.y)
        context.line_to(500, self.y)
        context.move_to(self.x, 0)
        context.line_to(self.x, 500)

        if self.orientation == VERTICAL:
            context.move_to(0, self.y)
            context.line_to(500, self.y)
        elif self.orientation == HORIZONTAL:
            context.move_to(self.x, 0)
            context.line_to(self.x, 500)
        context.set_source_rgba(0.0, 0.0, 0.75, 1.0)
        context.stroke()
