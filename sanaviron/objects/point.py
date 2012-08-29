#!/usr/bin/python
# -*- coding: utf-8 -*-

from holder import Holder

class Point(Holder):
#class Point():
    """This class represents a point"""

    def __init__(self):
        Holder.__init__(self)
        self.x, self.y = 0, 0
