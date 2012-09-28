#!/usr/bin/python
# -*- coding: utf-8 -*-

import pango
import pangocairo
from object import Object
from scale import Scale
from objects import *
import gtk

class Text(Object, gtk.Editable):
    """This class represents a text"""
    __name__ = "Text"

    def __init__(self, text = _("enter text here")):
        Object.__init__(self)

        self.font = "Verdana"
        self.size = 32
        self.preserve = False
        self.text = text
        self.foreground = "#000" # TODO

    def get_properties(self):
        Object.get_properties(self) + ["font", "size", "preserve", "text", "foreground"]

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        self.handler.control[NORTH].x = self.x + self.width / 2
        self.handler.control[NORTH].y = self.y
        self.handler.control[SOUTH].x = self.x + self.width / 2
        self.handler.control[SOUTH].y = self.y + self.height
        self.handler.control[WEST].x = self.x
        self.handler.control[WEST].y = self.y + self.height / 2
        self.handler.control[EAST].x = self.x + self.width
        self.handler.control[EAST].y = self.y + self.height / 2

    def draw(self, context):
        context.save()

        context = pangocairo.CairoContext(context) # XXX
        layout = pangocairo.CairoContext.create_layout(context)
        fontname = self.font
        if fontname.endswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): # XXX
            description = fontname
        else:
            size = int(self.size)
            description = "%s %d" % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        text = self.get_property('text')
        layout.set_markup(text)

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        #context.set_source_rgb(1.0, 0.0, 0.0)
        context.move_to(self.x, self.y)

        if bool(self.preserve):
            layout.set_width(int(self.width) * pango.SCALE)
            width, height = layout.get_size()
            height /= pango.SCALE
            self.height = height
        else:
            width, height = layout.get_size()
            width /= pango.SCALE
            height /= pango.SCALE
            self.scale(context, width, height)

        context.show_layout(layout)
        context.restore()
        Object.draw(self, context)

    def scale(self, context, width, height):
        if not self.width:
            self.width = width

        if not self.height:
            self.height = height

        scale = Scale()
        scale.horizontal = self.width / width
        scale.vertical = self.height / height

        if scale.horizontal:
            context.scale(scale.horizontal, 1.0)

        if scale.vertical:
            context.scale(1.0, scale.vertical)
