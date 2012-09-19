#!/usr/bin/env python
# -*- coding: utf-8 -*-

from holder import Holder

class Document(Holder):
    """This class represent a document"""

    def __init__(self):
        Holder.__init__(self)

        self.colors = list()
        self.pages = list()

    def draw(self, context, border, zoom, hints):
        for i, page in enumerate(self.pages):
            page.y = i * page.height + border * (i + 1) / zoom
            page.x = border / zoom

            page.draw(context, hints)

    def serialize(self):
        text = "<document>\n"
        text += "\t<definitions>\n"
        for color in self.colors:
            text += color.serialize()
        text += "\t</definitions>\n"
        text += "\t<layout>\n"
        for page in self.pages:
            text += page.serialize()
        text += "\t</layout>\n"
        text += "</document>\n"
        return text
