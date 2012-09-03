#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from object import Object
from point import Point
from objects import *


class Line(Object):
    """This class represents a line"""
    __name__ = "Line"

    def __init__(self):
        Object.__init__(self)
        self.handler.line = True
        self.dash = list()

        self.set_property("arrow-tip-length", 4 * 4)
        self.set_property("arrow-length", 8 * 4)
        self.set_property("arrow-width", 3 * 4)

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height

    def draw(self, context):
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)

        # arrow
        #arrow_tip_length = self.get_property("arrow-tip-length")
        arrow_length = self.get_property("arrow-length")
        arrow_width = self.get_property("arrow-width")

        width = arrow_width / 2
        length = math.sqrt(width * width + arrow_length * arrow_length)
        degrees = math.tan(width / length)
        angle = math.atan2(self.height, self.width) + math.pi
        a = Point()
        b = Point()
        a.x = self.x + self.width + length * math.cos(angle - degrees)
        a.y = self.y + self.height + length * math.sin(angle - degrees)
        b.x = self.x + self.width + length * math.cos(angle + degrees)
        b.y = self.y + self.height + length * math.sin(angle + degrees)

        context.fill_preserve()
        context.stroke()

        # line
        context.move_to(self.x, self.y)
        context.line_to(self.x + self.width, self.y + self.height)

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()

        context.move_to(self.x + self.width, self.y + self.height)
        context.line_to(a.x, a.y)
        context.line_to(b.x, b.y)
        context.line_to(self.x + self.width, self.y + self.height)
        context.stroke()

        Object.draw(self, context)
