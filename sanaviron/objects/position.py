#!/usr/bin/python
# -*- coding: utf-8 -*-

from holder import Holder
from point import Point

class Position(Holder, Point):
    """This class represents a position"""

    def __init__(self):
        Holder.__init__(self)
        Point.__init__(self)
