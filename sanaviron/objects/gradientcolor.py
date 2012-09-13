#!/usr/bin/python
# -*- coding: utf-8 -*-

from color import Color

class GradientColor(Color):
    """This class represents a gradient color"""

    __name__ = "GradientColor"

    def __init__(self, r, g, b, a, pos):
        Color.__init__(self, r, g, b, a)
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
        self.position = pos

    def get_xxx(self):
        return Color.get_xxx(self) + ['position']

    def __repr__(self):
        return str([self.red,self.green,self.blue,self.alpha,self.position])