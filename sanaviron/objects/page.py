#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paper import Paper
from holder import Holder

class Page(Paper):
    """This class represents a single document page"""

    def __init__(self):
        #Holder.__init__(self)
        Paper.__init__(self)

        self.children = list()

    def draw(self, context, hints):
        Paper.draw(self, context)
        for child in sorted(self.children, key=lambda child: child.z):
            child.hints = hints # TODO Not here
            child.draw(context)