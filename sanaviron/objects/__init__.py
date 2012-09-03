#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['NONE', 'NORTHWEST', 'NORTH', 'NORTHEAST', 'WEST', 'EAST', 'SOUTHWEST', 'SOUTH', 'SOUTHEAST', 'ANONIMOUS',
           'MANUAL', 'AUTOMATIC', 'COLOR', 'GRADIENT', 'PATTERN', 'LINEAR', 'RADIAL', 'HORIZONTAL', 'VERTICAL',
           'CENTIMETERS', 'MILLIMETERS', 'DOTS', 'INCHES', 'RADIANS', 'DEGREES', 'grad2rad', 'rad2grad',
           'angle_from_coordinates']

#import localization
from math import pi, atan2

NONE = -1
NORTHWEST = 0
NORTH = 1
NORTHEAST = 2
WEST = 3
EAST = 4
SOUTHWEST = 5
SOUTH = 6
SOUTHEAST = 7
ANONIMOUS = 8

MANUAL = 1
AUTOMATIC = 2

# fill type, type NONE present
COLOR = 0
GRADIENT = 1
PATTERN = 3

# gradient types
LINEAR = 0
RADIAL = 1

# orientation types
VERTICAL = 0
HORIZONTAL = 1

# units
CENTIMETERS = _("centimeters")
MILLIMETERS = _("millimeters")
DOTS = _("dots")
INCHES = _("inches")
RADIANS = _("radians")
DEGREES = _("degrees")


def grad2rad(grad):
    return float(grad) * pi / 180.0


def rad2grad(rad):
    return float(rad) * 180 / pi


def angle_from_coordinates(x, y, x0, y0, a, b):  #calculation of the angle from coordinates
    x = x - x0
    y = y - y0
    x /= a
    y /= b
    ang = atan2(y, x)
    ang = rad2grad(ang)
    if ang < 0:
        ang += 360
    return ang


def opossite(direction, orientation):
    if orientation == HORIZONTAL:
        if direction == NORTHEAST:
            return NORTHWEST
        if direction == EAST:
            return WEST
        if direction == SOUTHEAST:
            return SOUTHWEST
        if direction == NORTHWEST:
            return NORTHEAST
        if direction == WEST:
            return EAST
        if direction == SOUTHWEST:
            return SOUTHEAST
    elif orientation == VERTICAL:
        if direction == NORTHEAST:
            return SOUTHEAST
        if direction == NORTH:
            return SOUTH
        if direction == NORTHWEST:
            return SOUTHWEST
        if direction == SOUTHEAST:
            return NORTHEAST
        if direction == SOUTH:
            return NORTH
        if direction == SOUTHWEST:
            return NORTHWEST

    return NONE