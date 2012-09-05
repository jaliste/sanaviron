#!/usr/bin/python
# -*- coding: utf-8 -*-

AUTOMATIC = "AUTOMATIC"

class Property(dict):
    """This class represents a single typed and XML representable/serializable property"""

    def __repr__(self):
        return self.serialize()

    def __init__(self, name, value, type_name=AUTOMATIC):
        dict.__init__(self)
        self.name = name
        if type_name == AUTOMATIC:
            self.type = str(type(value)).split("'")[1]
            self.value = value
        else:
            self.type = type_name
            self.value = eval('%s("%s")' % (type_name, value))

    def serialize(self):
        return "<property name=\"%s\" type=\"%s\" value=\"%s\"/>" % (self.type, self.name, self.value)

class Properties(dict):
    """This class represents a collection of properties"""

    def __init__(self):
        dict.__init__(self)

    def append(self, property):
        self[property.name] = property

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
        #self.x = 0
        #self.y = 0
        #self.z = 0
        #self.width = 0
        #self.height = 0

    def __setattr__(self, name, value):
        #print "__setattr__ %s" % name
        if name in [ "x", "y", "z", "width", "height" ]:
            self.set_property(name, value)
        else:
            super(Holder, self).__setattr__(name, value)

    def __getattr__(self, name):
        #print "__getattr__ %s" % name
        if name in [ "x", "y", "z", "width", "height" ]:
            #value = self.get_property(name)
            #return int(round(float(value)))
            return self.get_property(name)
        return super(Holder, self).__getattr__(name)

    def get_type_name(self, value):
        return str(type(value)).split("'")[1]

    def get_typed_value(self, value, type):
        return eval('%s("%s")' % (type, value))

    def set_property(self, name, value, type=AUTOMATIC):
        self.properties.append(Property(name, value, type))

    def get_property(self, name):
        return self.properties[name].value

    def serialize(self):
        representation = "\t<object type=\"%s\">\n" % self.__name__
        representation += self.properties.serialize()
        representation += "\t</object>\n"
        return representation
