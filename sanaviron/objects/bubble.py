#!/usr/bin/python
# -*- coding: utf-8 -*-

from object import Object
from control import Control
from math import pi
from objects import *

class Bubble(Object):
    """This class represents a bubble"""

    __name__ = "Bubble"

    def __init__(self):
        Object.__init__(self)
        self.radius = 10
        self.distance = 10
        self.handler.control.append(Control())

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

        self.handler.control[8].x = self.x + self.radius + self.distance
        self.handler.control[8].y = self.y
        self.handler.control[8].limbus = True

    def draw(self, context):
        ###context.save()
        radius = self.radius

        dash = list()
        context.set_dash(dash)
        context.set_line_width(self.thickness)

        if radius > (self.height / 2) or radius > (self.width / 2):
            if (self.height / 2) < (self.width / 2):
                radius = self.height / 2
            else:
                radius = self.width / 2

        context.move_to(self.x, self.y + radius + self.distance)
        context.arc(self.x + radius, self.y + radius + self.distance, radius, pi, -pi / 2)
        context.curve_to(self.x + radius, self.y + self.distance,
            self.x + radius + self.distance, self.y + self.distance,
            self.x + radius + self.distance, self.y)
        context.curve_to(self.x + radius + self.distance, self.y,
            self.x + radius + self.distance, self.y + self.distance,
            self.x + self.width - radius, self.y + self.distance)
        context.arc(self.x + self.width - radius, self.y + radius + self.distance, radius, -pi / 2, 0)
        context.line_to(self.x + self.width, self.y + self.height - radius)
        context.arc(self.x + self.width - radius, self.y + self.height - radius, radius, 0, pi / 2)
        context.line_to(self.x + radius, self.y + self.height)
        context.arc(self.x + radius, self.y + self.height - radius, radius, pi / 2, pi)
        context.close_path()

        context.set_source_rgba(self.fill_color.red, self.fill_color.green,
            self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)
        ###context.restore()
