#!/usr/bin/python
# -*- coding: utf-8 -*-

AUTOMATIC = "AUTOMATIC"

fundamentals = ["x", "y", "z", "width", "height"]

def bool(value):
    return eval("%s" % str(value))

class Property(dict):
    """This class represents a single typed and XML representable/serializable property"""

    def __repr__(self):
        return self.serialize()

    def __init__(self, name, value, type=AUTOMATIC):
        dict.__init__(self)
        self.name = name
        if type == AUTOMATIC:
            self.type = self.get_type_from_value(value)
            self.value = value
        else:
            self.type = type
            self.value = eval('%s("%s")' % (type, value))

    def get_type_from_value(self, value):
        return str(type(value)).split("'")[1]

    def serialize(self):
        return "<property name=\"%s\" type=\"%s\" value=\"%s\"/>" % (self.name, self.type, self.value)

class Properties(dict):
    """This class represents a collection of properties"""

    def __init__(self):
        dict.__init__(self)

    def set_property(self, property):
        self[property.name] = property

    #def get_property(self, name):
    #    return self[name].get_value()

    def serialize(self):
        representation = ""
        for property in self.values():
            representation += "\t\t%s\n" % property.serialize()
        return representation

class Holder(object):
    """This class represents a object properties container"""

    def __repr__(self):
            return self.serialize()

    def __init__(self):
        self.properties = Properties()

    def __setattr__(self, name, value):
        if name in fundamentals:
            self.set_property(name, value)#, "float")
        else:
            super(Holder, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in fundamentals:
            return self.get_property(name)
        return super(Holder, self).__getattr__(name)

    def set_property(self, name, value, type=AUTOMATIC):
        self.properties.set_property(Property(name, value, type))

    def get_property(self, name):
        #return self.properties.get_property(name)
        return self.properties[name].value

    def serialize(self):
        representation = "\t<object type=\"%s\">\n" % self.__name__
        representation += self.properties.serialize()
        representation += "\t</object>\n"
        return representation
