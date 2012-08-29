#!/usr/bin/python
# -*- coding: utf-8 -*-

from holder import Holder


class Size(Holder):
    """This class represents a size"""

    def __init__(self):
        Holder.__init__(self)
        self.width = 0
        self.height = 0

        #def __getattr__(self, name):
        #  return self.get_property(name)

        #def __setattr__(self, name, value):
        #  self.set_property(name, value)
