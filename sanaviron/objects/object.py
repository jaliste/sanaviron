#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler import Handler
from rectangle import Rectangle
from color import Color
from point import Point
from size import Size
from objects import opossite, get_side
from objects import *

import gtk
import cairo
import pango
import pangocairo
import platform
import math

class Object(Rectangle):
    """This class represents the parent of all draweable objects"""

    def __init__(self):
        #self.id = random.uniform(0, 999999999)
        Rectangle.__init__(self)
        self.handler = Handler()
        self.offset = Rectangle()
        self.pivot = Point()
        self.selected = False
        self.resizing = False
        self.direction = NONE
        self.control = AUTOMATIC
        self.z = 0

        self.dash = []
        self.hints = False
        self.fill_style = COLOR
        self.fill_color = Color(0.25, 0.25, 0.25, 0.25)
        self.stroke_color = Color(0.25, 0.25, 0.25, 1)
        self.set_property("fill_color", str(self.fill_color))
        self.set_property("stroke_color", str(self.stroke_color))
        #self.set_gradient(Gradient())
        self.thickness = 1.0

    def post(self):
        pass

    def set_fill_style(self, fill_style):
        self.fill_style = fill_style
        self.set_property("fill_style", fill_style)

    def set_gradient(self, gradient):
        self.gradient = gradient
        self.set_property("gradient", gradient)

    def set_fill_color(self, color=Color()):
        self.fill_color = color
        self.set_property("fill_color", str(self.fill_color))

    def set_stroke_color(self, color=Color()):
        self.stroke_color = color
        self.set_property("stroke_color", str(self.stroke_color))

    def get_properties(self):
        if self.fill_style == COLOR:
            temp = self.get_property("fill_color")
            color = Color()
            color.set_color_as_string(temp)
            self.fill_color = color
        elif self.fill_style == GRADIENT:
            self.gradient = self.get_property("gradient")
        elif self.fill_style == PATTERN:
            self.gradient = self.get_property("pattern")

    def draw_hints(self, context):
        radius = 12.5
        offset = 6

        context.save()
        context.new_path()
        context.arc(self.x - radius, self.y - radius, radius, 0, 2 * math.pi)
        context.set_source_rgba(229 / 255.0, 122298 / 255.0, 0.0, 0.5)
        context.fill_preserve()
        context.set_line_width(2)
        context.set_source_rgb(122 / 255.0, 128 / 255.0, 54 / 255.0)
        context.stroke()

        context = pangocairo.CairoContext(context)
        layout = pangocairo.CairoContext.create_layout(context)
        if platform.system() == 'Windows':
            fontname = 'Sans'
        else:
            fontname = 'Ubuntu'
        text = str(int(self.z))
        if len(text) > 3:
            size = 6
            text = text[:3] + "..."
        elif len(text) > 2:
            size = 8
        elif len(text) > 1:
            size = 10
        else:
            size = 12
        description = '%s Bold %d' % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        layout.set_text(text)
        context.set_source_rgb(0, 0, 0)
        width, height = layout.get_size()
        width /= pango.SCALE
        height /= pango.SCALE
        context.move_to(self.x - radius - width / 2, self.y - radius - height / 2)
        context.show_layout(layout)
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        context.restore()

    def draw(self, context):
        if self.hints:
            self.draw_hints(context)

        ###context.save()
        if self.selected:
            self.handler.x = self.x
            self.handler.y = self.y
            self.handler.width = self.width
            self.handler.height = self.height
            self.post()
            self.handler.draw(context)
        ###context.restore()

    def at_position(self, x, y):
        if len(self.handler.control) < 1:
            return False
        return (x >= (self.x - self.handler.control[0].size / 2.0)) and\
               (x <= (self.x + self.width + self.handler.control[0].size / 2.0)) and\
               (y >= (self.y - self.handler.control[0].size / 2.0)) and\
               (y <= (self.y + self.height + self.handler.control[0].size / 2.0))

    def in_region(self, x, y, width, height):
        if width < 0:
            x += width
            width = -width
        if height < 0:
            y += height
            height = -height
        return (x + width) > self.x and (y + height) > self.y and\
               x < (self.x + self.width) and y < (self.y + self.height)

    def in_selection(self, selection):
        return self.in_region(selection.x, selection.y, selection.width, selection.height)

    def transform(self, x, y):
        pass

    def get_cursor(self, direction):
        if direction == NORTHWEST:
            cursor = gtk.gdk.TOP_LEFT_CORNER
        elif direction == NORTH:
            cursor = gtk.gdk.TOP_SIDE
        elif direction == NORTHEAST:
            cursor = gtk.gdk.TOP_RIGHT_CORNER
        elif direction == WEST:
            cursor = gtk.gdk.LEFT_SIDE
        elif direction == EAST:
            cursor = gtk.gdk.RIGHT_SIDE
        elif direction == SOUTHWEST:
            cursor = gtk.gdk.BOTTOM_LEFT_CORNER
        elif direction == SOUTH:
            cursor = gtk.gdk.BOTTOM_SIDE
        elif direction == SOUTHEAST:
            cursor = gtk.gdk.BOTTOM_RIGHT_CORNER
        elif direction >= ANONIMOUS:
            cursor = gtk.gdk.CROSSHAIR
        else:
            cursor = gtk.gdk.ARROW

        return gtk.gdk.Cursor(cursor)

    def set_position(self, position):
        (self.x, self.y) = (position.x, position.y)

    def set_size(self, size):
        (self.width, self.height) = (abs(size.width), abs(size.height))

    def resize(self, x, y):
        direction = self.direction

        if direction == NONE:
            return False

        position = Point()
        position.x = self.x
        position.y = self.y

        size = Size()
        size.width = self.width
        size.height = self.height

        def set_pivot(direction):
            self.handler.control[direction].pivot = True
            self.handler.control[opossite(direction)].pivot = False

        side = get_side(direction)

        if side is not VERTICAL:
            size.width = x - self.pivot.x
            if size.width < 0:
                position.x = x
                if direction in [NORTHWEST, SOUTHEAST]:
                    set_pivot(SOUTHEAST)
                elif direction in [SOUTHWEST, NORTHEAST]:
                    set_pivot(SOUTHWEST)
                else:
                    set_pivot(EAST)
            else:
                position.x = self.pivot.x
                if direction in [NORTHWEST, SOUTHEAST]:
                    set_pivot(NORTHWEST)
                elif direction in [SOUTHWEST, NORTHEAST]:
                    set_pivot(NORTHEAST)
                else:
                    set_pivot(WEST)

        if side is not HORIZONTAL:
            size.height = y - self.pivot.y
            if size.height < 0:
                position.y = y
                if direction in [NORTHWEST, SOUTHEAST]:
                    set_pivot(SOUTHEAST)
                elif direction in [SOUTHWEST, NORTHEAST]:
                    set_pivot(SOUTHWEST)
                else:
                    set_pivot(SOUTH)
            else:
                position.y = self.pivot.y
                if direction in [NORTHWEST, SOUTHEAST]:
                    set_pivot(NORTHWEST)
                elif direction in [SOUTHWEST, NORTHEAST]:
                    set_pivot(NORTHEAST)
                else:
                    set_pivot(NORTH)

        self.set_position(position)
        self.set_size(size)

        return True

    def move(self, x, y):
        self.x = x
        self.y = y