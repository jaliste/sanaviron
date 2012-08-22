#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler import Handler
from rectangle import Rectangle
from color import Color
from objects import *

class Object(Rectangle):
    """This class represents the parent of all draweable objects"""

    def __init__(self):
        #self.id = random.uniform(0, 999999999)
        Rectangle.__init__(self)
        self.handler = Handler()
        self.offset = Rectangle()
        self.selected = False
        self.resize = False
        self.direction = NONE
        self.control = AUTOMATIC
        self.z = 0

        self.dash = []
        self.fill_style = COLOR
        self.fill_color = Color(0.25, 0.25, 0.25, 0.25)
        self.stroke_color = Color(0.25, 0.25, 0.25, 1)
        self.set_property("fill_color", str(self.fill_color))
        self.set_property("stroke_color", str(self.stroke_color))
        #self.set_gradient(Gradient())
        self.thickness = 1.0

    def post(self):
        pass

    def set_fill_style(self, fill_style):
        self.fill_style = fill_style
        self.set_property("fill_style", fill_style)

    def set_gradient(self, gradient):
        self.gradient = gradient
        self.set_property("gradient", gradient)

    def set_fill_color(self, color=Color()):
        self.fill_color = color
        self.set_property("fill_color", str(self.fill_color))

    def set_stroke_color(self, color=Color()):
        self.stroke_color = color
        self.set_property("stroke_color", str(self.stroke_color))

    def get_properties(self):
        if self.fill_style == COLOR:
            temp = self.get_property("fill_color")
            color = Color()
            color.set_color_as_string(temp)
            self.fill_color = color
        elif self.fill_style == GRADIENT:
            self.gradient = self.get_property("gradient")
        elif self.fill_style == PATTERN:
            self.gradient = self.get_property("pattern")

    def draw(self, context):
        ###context.save()
        if self.selected:
            self.handler.x = self.x
            self.handler.y = self.y
            self.handler.width = self.width
            self.handler.height = self.height
            self.post()
            self.handler.draw(context)
            ###context.restore()

    def at_position(self, x, y):
        if len(self.handler.control) < 1:
            return False
        return (x >= (self.x - self.handler.control[0].size / 2.0)) and\
               (x <= (self.x + self.width + self.handler.control[0].size / 2.0)) and\
               (y >= (self.y - self.handler.control[0].size / 2.0)) and\
               (y <= (self.y + self.height + self.handler.control[0].size / 2.0))

    def in_region(self, x, y, width, height):
        if width < 0:
            x += width
            width = -width
        if height < 0:
            y += height
            height = -height
        return (x + width) > self.x and (y + height) > self.y and\
               x < (self.x + self.width) and y < (self.y + self.height)

    def in_selection(self, selection):
        return self.in_region(selection.x, selection.y, selection.width, selection.height)

    def transform(self, direction, x, y):
        pass

    def get_cursor(self, direction):
        pass