#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cairo
from object import Object
from scale import Scale
from objects import *

class Image(Object):
    """This class represents a image"""
    __name__ = "Image"

    def __init__(self, image=os.path.join("images", "logo.png")):
        Object.__init__(self)
        #self.image = image

        self.set_property('image', image)

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
        #//--pixbuf = gtk.gdk.pixbuf_new_from_file(self.image)
        #scaled = pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_HYPER)
        #//--scaled = pixbuf.scale_simple(int(self.width), int(self.height), gtk.gdk.INTERP_HYPER)

        #if not scaled:
        #  return

        #try: # FIXME
        #  context.set_source_pixbuf(scaled, self.x, self.y)
        #except:
        if 1:
            #pixmap, mask = pixbuf.render_pixmap_and_mask()
            #context.set_source_pixmap(mask, self.x, self.y)
            #surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
            image = self.get_property('image')
            surface = cairo.ImageSurface.create_from_png(image)
            #x = surface.get_width() / self.width
            #y = surface.get_height() / self.height
            width = surface.get_width()
            height = surface.get_height()
            #//context.save()
            #context.scale(x, y)
            x, y = self.scale(context, width, height)
            #context.set_source_surface(surface, 0, 0)
            context.set_source_surface(surface, self.x / x, self.y / y)
            #context.save()
            #context.move_to(self.x, self.y)
            #context.restore()
            #//context.restore()

        ##context.paint()
        context.paint()
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
        else:
            scale.horizontal = 1

        if scale.vertical:
            context.scale(1.0, scale.vertical)
        else:
            scale.vertical = 1

        return (scale.horizontal, scale.vertical)
