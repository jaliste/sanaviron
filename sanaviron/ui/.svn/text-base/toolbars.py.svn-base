#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import gobject

from ui.stock import *


class HorizontalToolbar(gtk.VBox):
    """This class represents a horizontal toolbar"""

    def __init__(self):
        gtk.VBox.__init__(self)

        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.add(toolbar)

        position = 0
        button = gtk.ToolButton(gtk.STOCK_NEW)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "new")

        position += 1
        button = gtk.ToolButton(gtk.STOCK_OPEN)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "open")

        position += 1
        button = gtk.ToolButton(gtk.STOCK_SAVE)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_PRINT_PREVIEW)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_PRINT)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_UNDO)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_CUT)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "cut")

        position += 1
        button = gtk.ToolButton(gtk.STOCK_COPY)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "copy")

        position += 1
        button = gtk.ToolButton(gtk.STOCK_PASTE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "paste")

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_DELETE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "delete")

        #position += 1
        #separator = gtk.SeparatorToolItem()
        #toolbar.insert(separator, position)

        #position += 1
        #button = gtk.ToggleToolButton(gtk.STOCK_BOLD)
        #toolbar.insert(button, position)

        #position += 1
        #button = gtk.ToggleToolButton(gtk.STOCK_ITALIC)
        #toolbar.insert(button, position)

        #position += 1
        #button = gtk.ToggleToolButton(gtk.STOCK_UNDERLINE)
        #toolbar.insert(button, position)

        #position += 1
        #button = gtk.ToggleToolButton(gtk.STOCK_STRIKETHROUGH)
        #toolbar.insert(button, position)

        #position += 1
        #separator = gtk.SeparatorToolItem()
        #toolbar.insert(separator, position)

        #position += 1
        #button = gtk.MenuToolButton(LINE_STYLE_POINT_DASH)
        #toolbar.insert(button, position)
        #menu = gtk.Menu()
        #button.set_menu(menu)

        #menuitem = gtk.ImageMenuItem(LINE_STYLE_CONTINUOUS)
        #menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        #menuitem = gtk.ImageMenuItem(LINE_STYLE_POINT)
        #menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        #menuitem = gtk.ImageMenuItem(LINE_STYLE_DASH)
        #menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        #menuitem = gtk.ImageMenuItem(LINE_STYLE_POINT_DASH)
        #menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        #menu.show_all()

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.MenuToolButton(gtk.STOCK_ZOOM_FIT)
        toolbar.insert(button, position)
        menu = gtk.Menu()
        button.set_menu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_FIT)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_100)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_IN)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_OUT)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menu.show_all()

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToggleToolButton(MARGINS_ENABLED)
        button.set_active(True)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "margins")

        position += 1
        button = gtk.ToggleToolButton(GRID)
        button.set_active(True)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "grid")

        position += 1
        button = gtk.ToggleToolButton(GUIDES)
        button.set_active(True)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "guides")

        position += 1
        button = gtk.ToggleToolButton(SNAP_ENABLED)
        button.set_active(True)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "snap")

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(EXPORT_TO_PDF)
        button.connect("clicked", self.clicked, "export-to-pdf")
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToggleToolButton(GROUP)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(BRING_TO_FRONT)
        button.connect("clicked", self.clicked, "bring-to-front")
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(BRING_TO_BACK)
        button.connect("clicked", self.clicked, "bring-to-back")
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.MenuToolButton(ALIGN_OBJECTS_CENTER_BOTH)
        toolbar.insert(button, position)
        menu = gtk.Menu()
        button.set_menu(menu)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTHWEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTHEAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTHWEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTHEAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_WEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_BOTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_EAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_HORIZONTAL)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_VERTICAL)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menu.show_all()

        position += 1
        button = gtk.MenuToolButton(ALIGN_PAPER_CENTER_BOTH)
        toolbar.insert(button, position)
        menu = gtk.Menu()
        button.set_menu(menu)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTHWEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTHEAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTHWEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTHEAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_WEST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_BOTH)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_EAST)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_HORIZONTAL)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_VERTICAL)
        menu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menu.show_all()

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_HELP)
        button.connect("clicked", self.clicked, "help")
        toolbar.insert(button, position)

        #gobject.signal_new("new", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("open", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("save", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        #gobject.signal_new("cut", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("copy", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("paste", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        #gobject.signal_new("export-to-pdf", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        #gobject.signal_new("delete", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("grid", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("guides", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("snap", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("margins", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("help", HorizontalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

    def clicked(self, widget, data):
        self.emit(data, None)


class VerticalToolbar(gtk.VBox):
    """This class represents a vertical toolbar"""

    def __init__(self):
        gtk.VBox.__init__(self)

        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.add(toolbar)

        position = 0
        button = gtk.ToolButton(LINE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "line")

        position += 1
        button = gtk.ToolButton(ARC)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "arc")

        position += 1
        button = gtk.ToolButton(CURVE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "curve")

        position += 1
        button = gtk.ToolButton(CONNECTOR)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "connector")

        position += 1
        button = gtk.ToolButton(BOX)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "box")

        position += 1
        button = gtk.ToolButton(ROUNDED_BOX)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "rounded-box")

        position += 1
        button = gtk.ToolButton(BUBBLE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "bubble")

        position += 1
        button = gtk.ToolButton(TEXT)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "text")

        position += 1
        button = gtk.ToolButton(BARCODE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "barcode")

        position += 1
        button = gtk.ToolButton(TABLE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "table")

        position += 1
        button = gtk.ToolButton(CHART)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "chart")

        position += 1
        button = gtk.ToolButton(IMAGE)
        toolbar.insert(button, position)
        button.connect("clicked", self.clicked, "image")

        #gobject.signal_new("line", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("arc", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("curve", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("connector", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("box", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("rounded-box", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("bubble", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("text", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("barcode", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("table", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("chart", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        #gobject.signal_new("image", VerticalToolbar, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

    def clicked(self, widget, data):
        self.emit(data, None)
