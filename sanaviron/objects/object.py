#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler import Handler
from rectangle import Rectangle
from color import Color
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
        self.selected = False
        self.resize = False
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
        context.arc(self.x - radius / 2 - offset, self.y - radius / 2 - offset, radius, 0, 2 * math.pi)
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
        size = 8
        description = '%s Bold %d' % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        text = str(int(self.z))
        layout.set_markup(text)
        context.set_source_rgb(0, 0, 0)
        context.move_to(self.x - radius - offset, self.y - radius - offset) # TODO Center in the bubble
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

    def transform(self, direction, x, y):
        pass

    def get_cursor(self, direction):
        if direction == NORTHWEST:
            return gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER)
        elif direction == NORTH:
            return gtk.gdk.Cursor(gtk.gdk.TOP_SIDE)
        elif direction == NORTHEAST:
            return gtk.gdk.Cursor(gtk.gdk.TOP_RIGHT_CORNER)
        elif direction == WEST:
            return gtk.gdk.Cursor(gtk.gdk.LEFT_SIDE)
        elif direction == EAST:
            return gtk.gdk.Cursor(gtk.gdk.RIGHT_SIDE)
        elif direction == SOUTHWEST:
            return gtk.gdk.Cursor(gtk.gdk.BOTTOM_LEFT_CORNER)
        elif direction == SOUTH:
            return gtk.gdk.Cursor(gtk.gdk.BOTTOM_SIDE)
        elif direction == SOUTHEAST:
            return gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER)
        elif direction >= ANONIMOUS:
            return gtk.gdk.Cursor(gtk.gdk.CROSSHAIR)

        return gtk.gdk.Cursor(gtk.gdk.ARROW)
