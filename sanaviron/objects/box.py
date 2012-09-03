#!/usr/bin/python
# -*- coding: utf-8 -*-

from control import Control
from object import Object
from separator import Separator
from objects import *

class Box(Object):
    """This class represents a box"""

    __name__ = "Box"

    def __init__(self):
        Object.__init__(self)

        self.separators = list()

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        self.handler.control[NORTH].x = self.x + self.width / 2
        self.handler.control[NORTH].y = self.y
        self.handler.control[SOUTH].x = self.x + self.width / 2
        self.handler.control[SOUTH].y = self.y + self.height
        self.handler.control[WEST].x = self.x
        self.handler.control[WEST].y = self.y + self.height / 2
        self.handler.control[EAST].x = self.x + self.width
        self.handler.control[EAST].y = self.y + self.height / 2

    def draw(self, context):
        ###context.save()
        dash = list()
        context.set_dash(dash)
        context.set_line_width(self.thickness)
        context.rectangle(self.x, self.y, self.width, self.height)
        context.set_source_rgba(self.fill_color.red, self.fill_color.green,
            self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()

        for i, separator in enumerate(self.separators):
            separator.synchronize(self)
            separator.draw(context)
            self.handler.control[ANONIMOUS+i] = separator.control

        Object.draw(self, context)
        ###context.restore()

    def transform(self, direction, x, y):
        if len(self.separators) > 0:
            if direction >= ANONIMOUS:
                separator = self.separators[direction-ANONIMOUS]
                if separator.direction == VERTICAL and x >= self.x and x - self.x <= self.width:
                    separator.position = x - self.x
                elif separator.direction == HORIZONTAL and y >= self.y and y - self.y <= self.height:
                    separator.position = y - self.y

    def add_separator_vertical(self, position):
        print "add-separator-vertical"
        separator = Separator()
        separator.position = position
        separator.direction = VERTICAL
        #separator.synchronize(self)
        self.separators.append(separator)
        self.handler.control.append(separator.control)

    def add_separator_horizontal(self, position):
        separator = Separator()
        separator.position = position
        separator.direction = HORIZONTAL
        #separator.synchronize(self)
        self.separators.append(separator)
        self.handler.control.append(separator.control)
