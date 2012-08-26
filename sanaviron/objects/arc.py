#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from math import sin, cos

from control import Control
from gradientcolor import GradientColor
from gradient import  Gradient
from object import Object
from objects import *

class Arc(Object):
    """This class represents an arc"""

    __name__ = "Arc"

    def __init__(self):
        Object.__init__(self)

        self.angle_start = 0.0
        self.angle_stop = 360.0
        self.set_property("angle_start", self.angle_start)
        self.set_property("angle_stop", self.angle_stop)

        self.closed = False
        self.closed_at_centre = False
        self.set_property("closed", int(self.closed))
        self.set_property("closed_at_centre", int(self.closed_at_centre))

        self.handler.control.append(Control())
        self.handler.control.append(Control())

        #self.block = False

    def set_angle_start(self, ang):
        #self.angle_start = ang
        self.set_property("angle_start", ang)

    def set_angle_stop(self, ang):
        #self.angle_stop = ang
        self.set_property("angle_stop", ang)

    def get_properties(self):
        Object.get_properties(self)
        self.angle_start = self.get_property("angle_start")
        self.angle_stop = self.get_property("angle_stop")
        self.closed = int(self.get_property("closed"))
        if self.closed:
            self.closed_at_centre = int(self.get_property("closed_at_centre"))

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        #self.handler.control[NORTH].x = self.x + self.width / 2
        #self.handler.control[NORTH].y = self.y
        #self.handler.control[EAST].x = self.x + self.width
        #self.handler.control[EAST].y = self.y + self.height / 2
        #self.handler.control[SOUTH].x = self.x + self.width / 2
        #self.handler.control[SOUTH].y = self.y + self.height
        #self.handler.control[WEST].x = self.x
        #self.handler.control[WEST].y = self.y + self.height / 2

        self.handler.control[8].x = self.centre_x + self.radius_horizontal * cos(grad2rad(self.angle_start))
        self.handler.control[8].y = self.centre_y + self.radius_vertical * sin(grad2rad(self.angle_start))
        self.handler.control[8].limbus = True

        self.handler.control[9].x = self.centre_x + self.radius_horizontal * cos(grad2rad(self.angle_stop))
        self.handler.control[9].y = self.centre_y + self.radius_vertical * sin(grad2rad(self.angle_stop))
        self.handler.control[9].limbus = True

        #self.height = self.width

    def draw(self, context):
        self.get_properties()
        context.set_dash(self.dash)
        context.set_line_width(self.thickness)

        self.radius_horizontal = self.width / 2.0
        self.radius_vertical = self.height / 2.0
        self.centre_x = self.x + self.radius_horizontal
        self.centre_y = self.y + self.radius_vertical

        context.save()
        context.new_path()
        context.translate(self.centre_x, self.centre_y)
        if (self.radius_horizontal > 0) and (self.radius_vertical > 0):
            context.scale(self.radius_horizontal, self.radius_vertical)
        context.arc(0.0, 0.0, 1.0, grad2rad(self.angle_start), grad2rad(self.angle_stop))
        context.restore()

        if (self.angle_start == self.angle_stop) or (self.angle_start == 0.0 and self.angle_stop == 360.0) or\
           (self.angle_start == 360.0 and self.angle_stop == 0.0):
            closed = False
        else:
            closed = self.closed

        if closed:
            if self.closed_at_centre:
                context.line_to(self.centre_x, self.centre_y)
            context.close_path()

        if '--debug' in sys.argv:  #Debug mode
            self.fill_style = GRADIENT

        if self.fill_style == GRADIENT:
            self.gradient = Gradient(0, "1", self.x, self.y, self.x + self.width, self.y)
            for index in range(11):
                self.gradient.add_new_color(
                    GradientColor(index * 0.1 + 0.1, index * 0.1, index * 0.1, 1.0, index * 0.1))
            self.gradient.update()
            context.set_source(self.gradient.gradient)
            self.set_gradient(self.gradient)
        elif self.fill_style == COLOR:
            context.set_source_rgba(self.fill_color.red, self.fill_color.green,
                self.fill_color.blue, self.fill_color.alpha)
        context.fill_preserve()

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.stroke()
        Object.draw(self, context)

    def transform(self, direction, x, y):
        if direction == 8:
            x0 = self.x + self.radius_horizontal
            y0 = self.y + self.radius_vertical
        
            if (x < self.x) or (y < self.y):
                self.set_property("closed_at_centre", False)
            else:
                self.set_property("closed_at_centre", True)
        
            if (x > (self.width + self.x)) or (y > (self.height + self.y)):
                self.set_property("closed_at_centre", False)
        
            if (self.radius_horizontal > 0) and (self.radius_vertical > 0):
                ang = angle_from_coordinates(x, y, x0, y0, self.radius_horizontal,
                    self.radius_vertical)
                self.set_angle_start(ang)
        else:
            x0 = self.x + self.radius_horizontal
            y0 = self.y + self.radius_vertical
    
            if (x < self.x) or (y < self.y):
                self.set_property("closed_at_centre", int(False))
            else:
                self.set_property("closed_at_centre", int(True))
    
            if (x > (self.width + self.x)) or (y > (self.height + self.y)):
                self.set_property("closed_at_centre", int(False))
    
            if (self.radius_horizontal > 0) and (self.radius_vertical > 0):
                ang = angle_from_coordinates(x, y, x0, y0, self.radius_horizontal,
                    self.radius_vertical)
                self.set_angle_stop(ang)
