#!/usr/bin/python
# -*- coding: utf-8 -*-

from serializable import Serializable

class Point(Serializable):
    """This class represents a point"""

    __name__ = "Point"

    def __init__(self):
        Serializable.__init__(self)
        self.x, self.y = 0, 0

    def __add__(self, other):
        result = Point()
        (result.x, result.y) = (self.x + other.x, self.y + other.y)
        return result

    def get_properties(self):
        return ["x", "y"]

    def set_position(self, position):
        (self.x, self.y) = (position.x, position.y)