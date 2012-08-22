#!/usr/bin/python
# -*- coding: utf-8 -*-

from holder import Holder

class Color(Holder):
    """This class represents a color"""

    def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
        Holder.__init__(self)
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __str__(self):
        temp = str(self.red) + " " + str(self.green) + " " +\
               str(self.blue) + " " + str(self.alpha)
        return temp

    def __hex__(self):
        temp = self.to_hex(self.red) + self.to_hex(self.green) +\
               self.to_hex(self.blue) + self.to_hex(self.alpha)
        return temp

    def to_hex(self, number):   #number 0..1
        temp = hex(int(number * 255))[2:]
        if len(temp) != 2:
            temp = "0" + temp
        return temp

    def set_color_as_string(self, color="0 0 0 0"):
        self.red = float(color.split()[0])
        self.green = float(color.split()[1])
        self.blue = float(color.split()[2])
        self.alpha = float(color.split()[3])

    def set_color_as_hex(self, color="00000000"):
        self.red = float(int(color[0:2], 16)) / 255
        self.green = float(int(color[2:4], 16)) / 255
        self.blue = float(int(color[4:6], 16)) / 255
        self.alpha = float(int(color[6:], 16)) / 255