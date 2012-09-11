#!/usr/bin/python
# -*- coding: utf-8 -*-

class GradientColor:
    """This class represents a gradient color"""

    def __init__(self, r, g, b, a, pos):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a
        self.position = pos

    def __repr__(self):
        return " ".join([str(self.red),str(self.green),str(self.blue),str(self.alpha),str(self.position)])