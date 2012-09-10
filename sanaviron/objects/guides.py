#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
from rectangle import Rectangle
from objects import HORIZONTAL, VERTICAL

class Guides(Rectangle):
    """This class represets the auxiliary guides"""

    def __init__(self):
        Rectangle.__init__(self)
        self.active = True
        self.tags = list()

    def draw(self, context):
        ###context.save()
        context.set_antialias(cairo.ANTIALIAS_NONE)

        for tag in self.tags:
            tag.draw_guide(context)

        context.stroke()
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        ###context.restore()

    def add_tag(self, tag):
        tag.synchronize(self)
        self.tags.append(tag)