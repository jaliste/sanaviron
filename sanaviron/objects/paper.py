#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

from margins import Margins

class Paper(Margins):
    """This class represents a paper"""

    def __init__(self):
        Margins.__init__(self)

    def draw(self, context):
        context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        shadow = 5.0 / context.get_matrix()[0]
        context.set_line_width(1.0 / context.get_matrix()[0])
        context.rectangle(self.x, self.y, self.width, self.height)

        context.set_source_rgb(1.0, 1.0, 1.0)
        context.fill_preserve()

        context.set_source_rgb(0.0, 0.0, 0.0)
        dash = list()
        context.set_dash(dash)
        context.stroke()

        Margins.draw(self, context)

        context.set_source_rgba(0.0, 0.0, 0.0, 0.25)
        dash = list()
        context.set_dash(dash)

        context.set_line_width(shadow)
        context.move_to(self.x + self.width + shadow / 2.0, self.y + shadow)
        context.line_to(self.x + self.width + shadow / 2.0, self.y + self.height + shadow / 2.0)
        context.line_to(self.x + shadow, self.y + self.height + shadow / 2.0)
        context.stroke()
        context.restore()
