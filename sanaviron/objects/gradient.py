#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from objects import *
from gradientcolor import GradientColor
from holder import Holder


class Gradient(Holder):
    """This class represents a gradient"""

    __name__ = "Gradient"

    def __init__(self, type=LINEAR, name="", x=0, y=0, x1=1, y1=1):
        Holder.__init__(self)
        #self.__name__ = name
        self.type = type
        self.colors = [GradientColor(1, 1, 1, 1, 0), GradientColor(0, 0, 0, 1, 1)]
        self.x, self.y = x, y
        self.width, self.height = x1, y1
        if type == LINEAR:
            self.gradient = cairo.LinearGradient(x, y, x1, y1)
        elif type == RADIAL:
            self.gradient = cairo.RadialGradient(x, y, x1, y1, 10, 100)
        self.update()

    def get_xxx(self):
        return ['type', 'colors']

    def __repr__(self):
        return str(
            self.get_object())#" ".join([str(self.type), self.__name__, str(self.x), str(self.y), str(self.width), str(self.height),
        #str(self.colors)])

    def get_object(self):
        return {
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "colors": self.colors
        }

    def change_size( self, x, y, x1, y1):
        self.x, self.y = x, y
        self.width, self.height = x1, y1
        self.update()

    def clear(self):
        self.colors = []

    def set_position(self, index, position):
        self.colors[index].position = position
        self.update()

    def set_color(self, index, color):
        self.colors[index] = color
        self.update()

    def add_new_color(self, gradient_color):
        self.colors.append(gradient_color)
        self.update()


    def delete_color(self, position):
        if len(self.colors) > 1:
            self.colors[position] = []
            self.update()


    def insert_color(self, gradient_color, position):
        self.colors.insert(position, gradient_color)
        self.update()

    def change_type(self, type):
        self.type = type
        self.update()

    def update(self):
        #del(self.gradient)
        if self.type == LINEAR:###ToDo two type!!!
            self.gradient = cairo.LinearGradient(self.x, self.y, self.width, self.height)
        else:
            self.gradient = cairo.RadialGradient(self.x, self.y, self.width, self.height)
        for color in self.colors:
            self.gradient.add_color_stop_rgba(color.position, color.red, color.green, color.blue, color.alpha)
