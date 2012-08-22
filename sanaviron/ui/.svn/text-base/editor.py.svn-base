#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

from objects.canvas import TestingCanvas as Canvas
from ui.notification import Notification
from ui.stock import EXPAND_PROPERTIES, CONTRACT_PROPERTIES
from ui.properties import Properties
from ui.climber import Climber
from ui.pager import Pager
from ui.ruler import HorizontalRuler, VerticalRuler
from ui.layer_selector import LayerSelector

class Editor(gtk.HPaned):
    """This class represents the main editor"""

    def __init__(self):
        gtk.HPaned.__init__(self)

        self.canvas = Canvas()
        self.properties = Properties(self.canvas)

        self.canvas.connect("select", self.select)
        self.canvas.connect("edit-child", self.edit_child)
        self.canvas.connect("scroll-event", self.wheel)

        box = gtk.VBox()

        if 0:
            panel = gtk.VPaned()
            panel.pack1(box, True, False)

            #sourcepad = SourcePad()
            sourcepad = gtk.Label('TEST')
            panel.pack2(sourcepad, False, True)

            self.pack1(panel, True, False)
        else:
            self.pack1(box, True, False)

        self.pack2(self.properties, False, True)

        top = gtk.HBox()
        box.pack_start(top, False, False)

        notification = Notification()
        top.pack_start(notification, False, False)

        layer_selector = LayerSelector()
        alignment = gtk.Alignment(1.0, 0.5)
        alignment.add(layer_selector)
        top.pack_start(alignment, True, True)

        separator = gtk.VSeparator()
        top.pack_start(separator, False, False)

        #button = gtk.Button(">|")
        image = gtk.Image()
        image.set_from_stock(CONTRACT_PROPERTIES, gtk.ICON_SIZE_MENU)
        button = gtk.Button()
        button.add(image)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect("clicked", self.expand)
        self.expanded = False
        top.pack_start(button, False, False)

        table = gtk.Table()
        box.add(table)

        bottom = gtk.HBox()
        box.pack_start(bottom, False, False)

        self.climber = Climber(self.canvas)
        bottom.pack_start(self.climber, False, False)

        pager = Pager(self.canvas)
        alignment = gtk.Alignment(1.0, 0.5)
        alignment.add(pager)
        bottom.pack_start(alignment, True, True)

        self.horizontal_ruler = HorizontalRuler()
        table.attach(self.horizontal_ruler, 1, 2, 0, 1, gtk.FILL | gtk.EXPAND, 0)

        self.vertical_ruler = VerticalRuler()
        table.attach(self.vertical_ruler, 0, 1, 1, 2, 0, gtk.FILL | gtk.EXPAND)

        area = gtk.ScrolledWindow()
        area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        table.attach(area, 1, 2, 1, 2, gtk.FILL | gtk.EXPAND, gtk.FILL | gtk.EXPAND)

        self.canvas.horizontal_ruler = self.horizontal_ruler
        self.canvas.vertical_ruler = self.vertical_ruler
        area.add_with_viewport(self.canvas)

    def expand(self, widget):
        image = widget.get_children()[0]
        self.expanded ^= 1
        if self.expanded:
            #widget.set_label("<")
            image.set_from_stock(EXPAND_PROPERTIES, gtk.ICON_SIZE_MENU)
            self.get_children()[1].hide()
        else:
            #widget.set_label(">|")
            image.set_from_stock(CONTRACT_PROPERTIES, gtk.ICON_SIZE_MENU)
            self.get_children()[1].show()
        self.canvas.queue_draw()

    def select(self, widget, child):
        self.properties.select(child.__name__, child)

    def edit_child(self, widget, child):
        pass
        #print "edit", child

    def wheel(self, widget, event):
        if event.state & gtk.gdk.CONTROL_MASK:
            if event.direction == gtk.gdk.SCROLL_UP:
                self.canvas.zoom_in()
                self.climber.update()
            elif event.direction == gtk.gdk.SCROLL_DOWN:
                self.canvas.zoom_out()
                self.climber.update()
            self.horizontal_ruler.zoom = self.canvas.zoom
            return True

    def key_press(self, widget, event):
        pass

    def _select(self, widget, child, buffer):
        #print "Se seleccionó un objeto \"%s\"" % child.__name__
        #if child.__name__ == "Table":
        #if child.__name__ == "Text":
        #   if not child.x and not child.y:
        #     return

        #  textpad = TextPad()
        #  textpad.set_size_request(150, -1)
        #  textpad.show_all()
        #  self.canvas.put(textpad, child.x + self.canvas.origin.x, child.y + self.canvas.origin.y)
        if child.__name__ == "Text":
            text = child.get_property("text")
            #print "putting text \"%s\"" % text
            buffer.handler_disconnect(self.disconnect_handler)
            buffer.set_text(text)
            self.disconnect_handler = buffer.connect("changed", self.changed)

    def set_paper(self):
        for page in self.canvas.pages:
            page.x = 25
            page.y = 25

            page.width = 800
            page.height = 1500

            page.top = 25
            page.left = 25
            page.bottom = 25
            page.right = 25

            page.active = True

            self.canvas.grid.active = True
            self.canvas.grid.size = 16 # 31 # 32
            self.canvas.guides.active = True
            self.canvas.guides.size = 16 * 8 # 128

            self.canvas.grid.snap = True
