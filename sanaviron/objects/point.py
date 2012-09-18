#!/usr/bin/python
# -*- coding: utf-8 -*-

from holder import Holder

class Point(Holder):
    """This class represents a point"""

    def __init__(self):
        Holder.__init__(self)
        self.x, self.y = 0, 0

    def __add__(self, other):
        result = Point()
        (result.x, result.y) = (self.x + other.x, self.y + other.y)
        return result

    def set_position(self, position):
        (self.x, self.y) = (position.x, position.y)