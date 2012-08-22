#!/usr/bin/python
# -*- coding: utf-8 -*-

from object import Object
from objects import *


class Line(Object):
    """This class represents a line"""
    __name__ = "Line"

    def __init__(self):
        Object.__init__(self)
        self.handler.line = True
        self.dash = list()

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height

    def draw(self, context):
        ###context.save()
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)
        context.move_to(self.x, self.y)
        context.line_to(self.x + self.width, self.y + self.height)
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)
        ###context.restore()
