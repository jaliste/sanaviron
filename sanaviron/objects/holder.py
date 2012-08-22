#!/usr/bin/python
# -*- coding: utf-8 -*-


class Holder:
    """This class represents a object properties container"""

    def __repr__(self):
            return self.serialize()

    def __init__(self):
        self.properties = dict()
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = 0
        self.height = 0

    def set_property(self, property, value):
        if value in [ "True", "False" ] and property != "text": # XXX
            value = eval(value)
        self.properties[property] = value

    def get_property(self, property):
        return self.properties[property]

    def serialize(self):
        type = self.__name__
        representation = "\t<object type=\"%s\">\n" % type
        representation += "\t\t<property internal=\"true\" name=\"x\" value=\"%s\"/>\n" % self.x
        representation += "\t\t<property internal=\"true\" name=\"y\" value=\"%s\"/>\n" % self.y
        representation += "\t\t<property internal=\"true\" name=\"z\" value=\"%s\"/>\n" % self.z
        representation += "\t\t<property internal=\"true\" name=\"width\" value=\"%s\"/>\n" % self.width
        representation += "\t\t<property internal=\"true\" name=\"height\" value=\"%s\"/>\n" % self.height
        for name in self.properties:
            value = self.properties[name]
            representation += "\t\t<property internal=\"false\" name=\"%s\" value=\"%s\"/>\n" % (name, value)
        representation += "\t</object>\n"

        return representation
