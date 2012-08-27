#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import gobject
import sys

from ui.stock import *
from objects import HORIZONTAL, VERTICAL

class Toolbar(gtk.Toolbar):
    """This class represents a toolbar"""

    def __init__(self, orientation=VERTICAL):
        gtk.Toolbar.__init__(self)

        if orientation == HORIZONTAL:
            self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        elif orientation == VERTICAL:
            self.set_orientation(gtk.ORIENTATION_VERTICAL)

        self.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        self.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)

        self.position = 0
        self.submenu = None

    def append(self, stock, signal):
        button = gtk.ToolButton(stock)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.position += 1

    def append_toggle(self, stock, signal):
        button = gtk.ToggleToolButton(stock)
        button.set_active(True)
        self.insert(button, self.position)
        button.connect("clicked", self.clicked, signal)
        self.position += 1

    def append_separator(self):
        separator = gtk.SeparatorToolItem()
        self.insert(separator, self.position)
        self.position += 1

    def append_with_submenu(self, stock, signal=None):
        button = gtk.MenuToolButton(stock)
        self.insert(button, self.position)
        if signal:
            button.connect("clicked", self.clicked, signal)
        self.submenu = gtk.Menu()
        print self.submenu
        button.set_menu(self.submenu)
        self.submenu.show_all()
        self.position += 1

    def append_to_submenu(self, stock, signal):
        menuitem = gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.clicked, signal)

    def clicked(self, widget, data):
        self.emit(data, None)

    def install_signal(self, signal):
        gobject.signal_new(signal, self.__class__, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))


class HorizontalToolbar(Toolbar):
    """This class represents a horizontal toolbar"""

    def __init__(self):
        Toolbar.__init__(self, HORIZONTAL)

        self.append(gtk.STOCK_NEW, "new")
        self.append(gtk.STOCK_OPEN, "open")
        self.append(gtk.STOCK_SAVE, "save")
        self.append_separator()
        self.append(gtk.STOCK_PRINT, "print")
        self.append_separator()
        self.append(gtk.STOCK_UNDO, "undo")
        self.append(gtk.STOCK_REDO, "redo")
        self.append_separator()
        self.append(gtk.STOCK_CUT, "cut")
        self.append(gtk.STOCK_COPY, "copy")
        self.append(gtk.STOCK_PASTE, "paste")
        self.append_separator()
        self.append(gtk.STOCK_DELETE, "delete")
        #self.append_separator()
        #self.append_toggle(gtk.STOCK_BOLD, "bold")
        #self.append_toggle(gtk.STOCK_ITALIC, "italic")
        #self.append_toggle(gtk.STOCK_UNDERLINE, "underline")
        #self.append_toggle(gtk.STOCK_STRIKEOUT, "strikeout")
        #self.append_separator()
        #self.append_to_submenu(LINE_STYLE_POINT_DASH, "line-style-point-dash")
        #self.append_to_submenu(LINE_STYLE_CONTINUOUS, "line-style-continuous")
        #self.append_to_submenu(LINE_STYLE_POINT, "line-style-point")
        #self.append_to_submenu(LINE_STYLE_DASH, "line-style-dash")
        self.append_separator()
        self.append_with_submenu(gtk.STOCK_ZOOM_FIT, "zoom-fit")
        self.append_to_submenu(gtk.STOCK_ZOOM_100, "zoom-100")
        self.append_to_submenu(gtk.STOCK_ZOOM_IN, "zoom-in")
        self.append_to_submenu(gtk.STOCK_ZOOM_OUT, "zoom-out")
        self.append_separator()
        self.append_toggle(MARGINS_ENABLED, "margins")
        self.append_toggle(GRID, "grid")
        self.append_toggle(GUIDES, "guides")
        self.append_toggle(SNAP_ENABLED, "snap")
        self.append_separator()
        self.append(EXPORT_TO_PDF, "export-to-pdf")
        self.append_separator()
        self.append_toggle(GROUP, "group")
        self.append_separator()
        self.append(BRING_TO_FRONT, "bring-to-front")
        self.append(BRING_TO_BACK, "bring-to-back")
        self.append_separator()

        self.append_with_submenu(ALIGN_OBJECTS_CENTER_BOTH, "align-object-center-both")
        self.append_to_submenu(ALIGN_OBJECTS_NORTHWEST, "align-object-northwest")
        self.append_to_submenu(ALIGN_OBJECTS_NORTH, "align-object-north")
        self.append_to_submenu(ALIGN_OBJECTS_SOUTHWEST, "align-object-southwest")
        self.append_to_submenu(ALIGN_OBJECTS_NORTHEAST, "align-object-northeast")
        self.append_to_submenu(ALIGN_OBJECTS_SOUTH, "align-object-south")
        self.append_to_submenu(ALIGN_OBJECTS_SOUTHEAST, "align-object-southeast")
        self.append_to_submenu(ALIGN_OBJECTS_WEST, "align-object-west")
        self.append_to_submenu(ALIGN_OBJECTS_EAST, "align-object-east")
        self.append_to_submenu(ALIGN_OBJECTS_CENTER_HORIZONTAL, "align-object-center-horizontal")
        self.append_to_submenu(ALIGN_OBJECTS_CENTER_VERTICAL, "align-object-center-vertical")

        self.append_with_submenu(ALIGN_PAPER_CENTER_BOTH, "align-paper-center-both")
        self.append_to_submenu(ALIGN_PAPER_NORTHWEST, "align-paper-northwest")
        self.append_to_submenu(ALIGN_PAPER_NORTH, "align-paper-north")
        self.append_to_submenu(ALIGN_PAPER_SOUTHWEST, "align-paper-southwest")
        self.append_to_submenu(ALIGN_PAPER_NORTHEAST, "align-paper-northeast")
        self.append_to_submenu(ALIGN_PAPER_SOUTH, "align-paper-south")
        self.append_to_submenu(ALIGN_PAPER_SOUTHEAST, "align-paper-southeast")
        self.append_to_submenu(ALIGN_PAPER_WEST, "align-paper-west")
        self.append_to_submenu(ALIGN_PAPER_EAST, "align-paper-east")
        self.append_to_submenu(ALIGN_PAPER_CENTER_HORIZONTAL, "align-paper-center-horizontal")
        self.append_to_submenu(ALIGN_PAPER_CENTER_VERTICAL, "align-paper-center-vertical")

        self.append_separator()
        self.append(gtk.STOCK_HELP, "help")

        self.install_signal("new")
        self.install_signal("open")
        self.install_signal("save")
        self.install_signal("cut")
        self.install_signal("copy")
        self.install_signal("paste")
        self.install_signal("export-to-pdf")
        self.install_signal("delete")
        self.install_signal("bring-to-front")
        self.install_signal("bring-to-back")
        self.install_signal("grid")
        self.install_signal("guides")
        self.install_signal("snap")
        self.install_signal("margins")
        self.install_signal("help")


class VerticalToolbar(Toolbar):
    """This class represents a vertical toolbar"""

    def __init__(self):
        Toolbar.__init__(self)

        self.set_style(gtk.TOOLBAR_ICONS)

        self.append(LINE, "line")
        self.append(ARC, "arc")
        self.append(CURVE, "curve")
        self.append(CONNECTOR, "connector")

        self.append_with_submenu(BOX, "box")
        self.append_to_submenu(SPLIT_HORIZONTALLY, "split-horizontally")
        self.append_to_submenu(SPLIT_VERTICALLY, "split-vertically")
        self.append_to_submenu(REMOVE_SPLIT, "remove-split")

        if '--debug' not in sys.argv:
            self.submenu.hide()

        self.append(ROUNDED_BOX, "rounded-box")
        self.append(BUBBLE, "bubble")
        self.append(TEXT, "text")
        self.append(BARCODE, "barcode")
        self.append(TABLE, "table")
        self.append(CHART, "chart")
        self.append(IMAGE, "image")

        self.install_signal("line")
        self.install_signal("arc")
        self.install_signal("curve")
        self.install_signal("connector")
        self.install_signal("box")
        self.install_signal("rounded-box")
        self.install_signal("bubble")
        self.install_signal("text")
        self.install_signal("barcode")
        self.install_signal("table")
        self.install_signal("chart")
        self.install_signal("image")
        self.install_signal("split-horizontally")
        self.install_signal("split-vertically")
        self.install_signal("remove-split")