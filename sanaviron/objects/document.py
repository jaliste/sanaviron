#!/usr/bin/env python
# -*- coding: utf-8 -*-

from holder import Holder

class Document(Holder):
    """This class represent a document"""

    __name__ = "Document"

    def __init__(self):
        Holder.__init__(self)

        self.pages = list()

    def draw(self, context, border, zoom, hints):
        for i, page in enumerate(self.pages):
            page.y = i * page.height + border * (i + 1) / zoom
            page.x = border / zoom

            page.draw(context, hints)

    def serialize(self):
        text = "<object type=\"%s\">" % self.__name__
        text += "<children>"
        for page in self.pages:
            text += page.serialize()
        text += "</children>"
        text += "</object>"
        return text
