#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['NONE', 'NORTHWEST', 'NORTH', 'NORTHEAST', 'WEST', 'EAST', 'SOUTHWEST', 'SOUTH', 'SOUTHEAST', 'ANONIMOUS',
           'MANUAL', 'AUTOMATIC', 'COLOR', 'GRADIENT', 'PATTERN', 'LINEAR', 'RADIAL', 'HORIZONTAL', 'VERTICAL',
           'CENTIMETERS', 'MILLIMETERS', 'DOTS', 'INCHES', 'RADIANS', 'DEGREES', 'TOP_LEFT', 'TOP', 'TOP_RIGHT',
           'RIGHT', 'BOTTOM_RIGHT', 'BOTTOM', 'BOTTOM_LEFT', 'LEFT', 'CENTER','print_text', 'grad2rad', 'rad2grad',
           'angle_from_coordinates', 'get_side', 'opposite', 'set_as_point']

import pango, pangocairo
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


#text align
TOP_LEFT = 0
TOP = 1
TOP_RIGHT = 2
RIGHT = 3
BOTTOM_RIGHT = 4
BOTTOM = 5
BOTTOM_LEFT = 6
LEFT = 7
CENTER = 8

def grad2rad(grad):
    return float(grad) * pi / 180.0


def rad2grad(rad):
    return float(rad) * 180 / pi


def angle_from_coordinates(x, y, x0, y0, a, b):
    """
    calculation of the angle from coordinates
    """
    x = x - x0
    y = y - y0
    x /= a
    y /= b
    ang = atan2(y, x)
    ang = rad2grad(ang)
    if ang < 0:
        ang += 360
    return ang


def get_side(direction):
    if direction in [EAST, WEST]:
        return HORIZONTAL
    elif direction in [NORTH, SOUTH]:
        return VERTICAL
    else:
        return NONE


def opposite(direction):
    if direction == NORTHEAST:
        return SOUTHWEST
    elif direction == NORTH:
        return SOUTH
    elif direction == NORTHWEST:
        return SOUTHEAST
    elif direction == SOUTHEAST:
        return NORTHWEST
    elif direction == SOUTH:
        return NORTH
    elif direction == SOUTHWEST:
        return NORTHEAST
    elif direction == WEST:
        return EAST
    elif direction == EAST:
        return WEST
    return NONE


def set_as_point(instance):
    instance.x = 0.0
    instance.y = 0.0

def context_align(context,rect,align,lw,lh,border):
    if align is TOP_LEFT:
        context.move_to(rect["x"] + border, rect["y"] + border)
    elif align is TOP:
        context.move_to(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect["y"] + border)
    elif align is TOP_RIGHT:
        context.move_to(rect['x'] + rect['w'] - lw - border,
                        rect["y"] + border)
    elif align is RIGHT:
        context.move_to(rect['x'] + rect['w'] - lw - border,
                        rect["y"] + (rect['h'] - lh) * 0.5)
    elif align is BOTTOM_RIGHT:
        context.move_to(rect['x'] + rect['w'] - lw - border * 2,
                        rect['y'] + rect['h'] - lh - border)
    elif align is BOTTOM:
        context.move_to(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect['y'] + rect['h'] - lh - border)
    elif align is BOTTOM_LEFT:
        context.move_to(rect['x'] + border,
                        rect['y'] + rect['h'] - lh - border)
    elif align is LEFT:
        context.move_to(rect['x'] + border,
                        rect["y"] + (rect['h'] - lh) * 0.5)
    elif align is CENTER:
        context.move_to(rect['x'] + (rect["w"] - lw) * 0.5,
                        rect["y"] + (rect['h'] - lh) * 0.5)


def print_text(context, text="", rect={'x': 0, 'y': 0, 'w': 1, 'h': 1},
               font="",
               font_name="Ubuntu",
               font_style="Normal", font_size=10,
               align=TOP_LEFT, border=4, spasing=0):
    context.save()
    if not font:
        font = " ".join([font_name, font_style, str(font_size)])
    layout = pangocairo.CairoContext.create_layout(context)
    desc = pango.FontDescription(font)
    layout.set_font_description(desc)
    layout.set_markup(str(text))

    if spasing:
        attr_list=pango.AttrList()
        attr = pango.AttrLetterSpacing(spasing*pango.SCALE,0,10000)
        attr_list.insert(attr)
        layout.set_attributes(attr_list)

    pangocairo.CairoContext.update_layout(context, layout)
    lw, lh = layout.get_size()
    lw /= pango.SCALE
    lh /= pango.SCALE
    context_align(context,rect,align,lw,lh,border)
    pangocairo.CairoContext.show_layout(context, layout)
    context.restore()
