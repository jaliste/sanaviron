#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from rectangle import Rectangle
from control import Control
from objects import NONE, ANONIMOUS

class Handler(Rectangle):
    """This class represents a rectangular control points handler"""

    def __init__(self):
        Rectangle.__init__(self)
        self.control = list()
        self.pivot = Control()
        self.pivot.pivot = True

        index = 0
        while index < ANONIMOUS:
            control = Control()
            self.control.append(control)
            index += 1
            self.line = False

    def draw_handler(self, context):
        if not self.line:
            context.set_antialias(cairo.ANTIALIAS_NONE)
            context.set_line_width(1.0 / context.get_matrix()[0])
            context.set_source_rgb(0.5, 0.5, 1.0)
            dash = []
            context.set_dash(dash)
            context.rectangle(self.x, self.y, self.width, self.height)
            context.stroke()
            context.set_antialias(cairo.ANTIALIAS_DEFAULT)

    def draw_controls(self, context):
        for control in self.control:
            control.draw(context)

    def draw_pivot(self, context):
        self.pivot.draw(context)

    def draw(self, context):
        self.draw_handler(context)
        self.draw_controls(context)
        self.draw_pivot(context)

    def at_position(self, x, y):
        #return x >= (self.x - self.width / 2) and x <= (self.x + self.width) and \
        #       y >= (self.y - self.height / 2) and y <= (self.y + self.height)
        for control in self.control:
            if control.at_position(x, y):
                return True

        return False

    def get_direction(self, x, y):
        direction = 0
        while direction < len(self.control):
            control = self.control[direction]
            if control.at_position(x, y):
                return direction
            direction += 1
        return NONE
