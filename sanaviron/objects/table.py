#!/usr/bin/python
# -*- coding: utf-8 -*-

import pango
import pangocairo
from object import Object
from objects import *
from control import Control

class Table(Object):
    """This class represents a table"""
    __name__ = "Table"

    def __init__(self, rows=5, columns="0", titles=_("Column 1")):
        Object.__init__(self)
        self.vertical_spacing = 5
        self.horizontal_spacing = 5

        self.control = MANUAL

        self.set_property("rows", rows)
        self.set_property("columns", columns)
        self.set_property("titles", titles)
        self.set_property("font", "Verdana")
        self.set_property("size", 16)

    def post(self):
        n_controls = len(self.handler.control)
        while n_controls > ANONIMOUS:
            n_controls -= 1
            del self.handler.control[n_controls]

        columns = self.get_property("columns").split(':')

        offset = 0

        for i, column in enumerate(columns):
            offset += int(column) + i * self.horizontal_spacing
            control = Control()
            self.handler.control.append(control)
            control.x = self.x + offset
            control.y = self.y + self.height / 2
            control.limbus = True

    def draw(self, context):
        ###context.save()

        rows = self.get_property("rows")
        rows = int(rows)
        columns = self.get_property("columns").split(':')
        n_columns = len(columns)

        titles = self.get_property("titles").split(':')
        #n_titles = len(titles)

        x, y = 0, 0
        self.width = 0
        self.height = 0

        context = pangocairo.CairoContext(context) # XXX
        total_width = 0

        for column in range(n_columns):
            for row in range(rows):
                layout = pangocairo.CairoContext.create_layout(context)
                fontname = self.get_property('font')
                if fontname.endswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")): # XXX
                    description = fontname
                else:
                    size = self.get_property('size')
                    size = int(size)
                    description = "%s %d" % (fontname, size)
                font = pango.FontDescription(description)
                layout.set_font_description(font)
                title = titles[column]
                layout.set_markup(title)

                if row == 0:
                    context.set_source_rgb(0.0, 0.0, 0.0)
                else:
                    context.set_source_rgb(0.75, 0.75, 0.75)

                width, height = layout.get_size()

                if columns[column] == '0':
                    width /= pango.SCALE
                    columns[column] = str(width)
                else:
                    width = int(columns[column])

                height /= pango.SCALE

                x = self.x + total_width + self.horizontal_spacing * column
                y = self.y + (self.vertical_spacing + height) * row

                context.move_to(x, y)
                context.show_layout(layout)

            self.height = (self.vertical_spacing + height) * rows

            total_width += width

        columns = ':'.join(columns)
        self.set_property("columns", columns)

        #self.height = rows * (self.vertical_spacing + height) - self.vertical_spacing
        self.width = n_columns * self.horizontal_spacing - self.horizontal_spacing + total_width
        ###context.restore()
        Object.draw(self, context)

    def get_cursor(self, direction):
        return gtk.gdk.Cursor(gtk.gdk.FLEUR)

    def transform(self, direction, x, y):
        direction -= ANONIMOUS
        columns = self.get_property("columns").split(':')
        n_columns = len(columns)
        offset = self.x
        if direction < n_columns:
            for column in range(direction):
                offset += int(columns[column]) + self.horizontal_spacing
            columns[direction] = str(int(x - offset))
        columns = ':'.join(columns)
        self.set_property("columns", columns)
