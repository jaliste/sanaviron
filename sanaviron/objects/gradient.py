#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from objects import *
#from gradientcolor import GradientColor


class Gradient:
    """This class represents a gradient"""

    def __init__(self, type=LINEAR, name="", x=0, y=0, x1=1, y1=1):
        #Holder.__init__(self)
        self.__name__ = name
        self.type = type
        self.colors = list()
        self.x = x
        self.y = y
        self.width = x1
        self.height = y1
        if type == LINEAR:
            self.gradient = cairo.LinearGradient(x, y, x1, y1)
        elif type == RADIAL:
            self.gradient = cairo.RadialGradient(x, y, x1, y1, 10, 100)

            #   for index in range(11):

    #    self.add_new_color(GradientColor( index*0.1 + 0.1, index*0.1, index*0.1,1.0, index*0.1))
    #   self.update()

    def change_size( self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.width = x1
        self.height = y1
        self.update()


    def set_position(self, index, position):
        self.colors[index].position = position


    def add_new_color(self, gradient_color):
        self.colors.append(gradient_color)


    def delete_color(self, position):
        self.colors[position] = []


    def insert_color(self, gradient_color, position):
        self.colors.insert(position, gradient_color)


    def change_type(self, type):
        self.type = type


    def update(self):
        #del(self.gradient)
        self.gradient = cairo.LinearGradient(self.x, self.y, self.width, self.height)
        for color in self.colors:
            self.gradient.add_color_stop_rgba(color.position, color.red, color.green, color.blue, color.alpha)
