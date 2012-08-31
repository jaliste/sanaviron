#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
import gobject
import sys
from ui.stock import *

class MenuBar(gtk.MenuBar):
    """This class represents a pull-down menu bar"""

    def __init__(self):
        gtk.MenuBar.__init__(self)
        self.connect("realize", self.realize)

        self.bindings = gtk.AccelGroup()
        self.stack = None
        self.submenu = None
        self.signals = list()

    def install_signal(self, signal):
        gobject.signal_new(signal, self.__class__, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,))

    def install_signals(self):
        for signal in self.signals:
            self.install_signal(signal)

    def append_menu(self, stock, descend=False, right=False):
        menuitem = gtk.ImageMenuItem(stock)
        if right:
            menuitem.set_right_justified(True)
        if descend:
            self.stack = self.submenu
            self.submenu.append(menuitem)
        else:
            self.append(menuitem)
        self.submenu = gtk.Menu()
        menuitem.set_submenu(self.submenu)

    def append_item(self, stock, signal, accelerator = None):
        menuitem = gtk.ImageMenuItem(stock)
        self.submenu.append(menuitem)
        menuitem.connect("activate", self.activate, signal)
        self.signals.append(signal)
        if accelerator:
            key, mask = gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("activate", self.bindings, key, mask, gtk.ACCEL_VISIBLE)

    def append_toggle(self, stock, signal, accelerator = None, toggled = True):
        info = gtk.stock_lookup(stock)
        label = info[1] if info else stock
        menuitem = gtk.CheckMenuItem(label)
        menuitem.set_active(toggled)
        self.submenu.append(menuitem)
        menuitem.connect("toggled", self.activate, signal)
        self.signals.append(signal)
        if accelerator:
            key, mask = gtk.accelerator_parse(accelerator)
            menuitem.add_accelerator("toggled", self.bindings, key, mask, gtk.ACCEL_VISIBLE)

    def append_separator(self):
        separator = gtk.SeparatorMenuItem()
        self.submenu.append(separator)

    def ascend(self):
        self.submenu = self.stack

    def realize(self, widget):
        toplevel = self.get_toplevel()
        toplevel.add_accel_group(self.bindings)

    def activate(self, widget, data):
        print data
        self.emit(data, None)


class Menu(MenuBar):
    """this class represents the application menu bar"""

    def __init__(self):
        MenuBar.__init__(self)

        self.append_menu("_" + _("File"))
        self.append_item(gtk.STOCK_NEW, "new", "<Control>N")
        self.append_item(gtk.STOCK_OPEN, "open", "<Control>O")
        self.append_item(gtk.STOCK_SAVE, "save", "<Control>S")
        self.append_item(gtk.STOCK_SAVE_AS, "save-as", "<Control><Shift>S")
        self.append_separator()
        self.append_item(gtk.STOCK_PAGE_SETUP, "page-setup")
        self.append_item(gtk.STOCK_PRINT_PREVIEW, "print-preview", "<Control><Shift>P")
        self.append_item(gtk.STOCK_PRINT, "print", "<Control>P")
        self.append_separator()
        self.append_menu("_" + _("Export"), True)
        self.append_item(EXPORT_TO_PDF, "export-to-pdf")
        self.ascend()
        self.append_separator()
        self.append_item(gtk.STOCK_QUIT, "quit", "<Control>Q")

        self.append_menu("_" + _("Edit"))
        self.append_item(gtk.STOCK_UNDO, "undo", "<Control>Z")
        self.append_item(gtk.STOCK_REDO, "redo", "<Control>Y")
        self.append_separator()
        self.append_item(gtk.STOCK_COPY, "copy", "<Control>C")
        self.append_item(gtk.STOCK_CUT, "cut", "<Control>X")
        self.append_item(gtk.STOCK_PASTE, "paste", "<Control>V")
        self.append_separator()
        self.append_item(gtk.STOCK_DELETE, "delete", "Delete")
        self.append_separator()
        self.append_item(gtk.STOCK_SELECT_ALL, "select-all", "<Control>A")

        self.append_menu("_" + _("View"))
        self.append_toggle(MARGINS_ENABLED, "margins")
        self.append_toggle(GRID, "grid")
        self.append_toggle(GUIDES, "guides")
        self.append_toggle(SNAP_ENABLED, "snap")
        self.append_toggle(_("Z-Order hint"), "hints", toggled = False)
        self.append_separator()
        self.append_toggle(gtk.STOCK_PROPERTIES, "properties")
        self.append_toggle(_("Menubar"), "menubar")
        self.append_toggle(_("Statusbar"), "statusbar")

        self.append_menu("_" + _("Insert"))
        self.append_item(LINE, "line")
        self.append_item(ARC, "arc")
        self.append_item(CURVE, "curve")
        self.append_item(CONNECTOR, "connector")
        self.append_menu(BOX, "box", True)
        self.append_item(BOX, "box")
        self.append_item(SPLIT_HORIZONTALLY, "split-horizontally")
        self.append_item(SPLIT_VERTICALLY, "split-vertically")
        self.append_item(REMOVE_SPLIT, "remove-split")
        self.ascend()
        self.append_item(ROUNDED_BOX, "rounded-box")
        self.append_item(BUBBLE, "bubble")
        self.append_item(TEXT, "text")
        self.append_item(TABLE, "table")
        self.append_item(CHART, "chart")
        self.append_item(BARCODE, "barcode")
        self.append_item(IMAGE, "image")

        self.append_menu("_" + _("Format"))
        self.append_item(gtk.STOCK_SELECT_FONT, "select-font")
        self.append_separator()
        self.append_item(gtk.STOCK_SELECT_COLOR, "select-color")

        self.append_menu("_" + _("Tools"))
        self.append_item(GROUP, "group", "<Control>G")
        self.append_item(UNGROUP, "ungroup", "<Control><Shift>G")
        self.append_separator()
        self.append_item(BRING_TO_FRONT, "bring-to-front", "<Control>plus")
        self.append_item(BRING_TO_BACK, "bring-to-back", "<Control>minus")
        self.append_separator()
        self.append_menu("_" + _("Zoom"), True)
        self.append_item(gtk.STOCK_ZOOM_FIT, "zoom-fit", "<Control>0")
        self.append_item(gtk.STOCK_ZOOM_100, "zoom-100", "<Control>1")
        self.append_item(gtk.STOCK_ZOOM_IN, "zoom-in", "<Control><Shift>plus")
        self.append_item(gtk.STOCK_ZOOM_OUT, "zoom-out", "<Control><Shift>minus")
        self.ascend()
        self.append_separator()
        self.append_menu("_" + _("Objects alignment"), True)
        self.append_item(ALIGN_OBJECTS_NORTHWEST, "align-objects-northwest")
        self.append_item(ALIGN_OBJECTS_NORTH, "align-objects-north")
        self.append_item(ALIGN_OBJECTS_NORTHEAST, "align-objects-northeast")
        self.append_item(ALIGN_OBJECTS_SOUTHWEST, "align-objects-southwest")
        self.append_item(ALIGN_OBJECTS_SOUTH, "align-objects-south")
        self.append_item(ALIGN_OBJECTS_SOUTHEAST, "align-objects-southeast")
        self.append_item(ALIGN_OBJECTS_WEST, "align-objects-west")
        self.append_item(ALIGN_OBJECTS_CENTER_BOTH, "align-objects-center-both")
        self.append_item(ALIGN_OBJECTS_EAST, "align-objects-east")
        self.append_item(ALIGN_OBJECTS_CENTER_HORIZONTAL, "align-objects-center-horizontal")
        self.append_item(ALIGN_OBJECTS_CENTER_VERTICAL, "align-objects-center-vertical")
        self.ascend()
        self.append_menu("_" + _("Paper alignment"), True)
        self.append_item(ALIGN_PAPER_NORTHWEST, "align-paper-northwest")
        self.append_item(ALIGN_PAPER_NORTH, "align-paper-north")
        self.append_item(ALIGN_PAPER_NORTHEAST, "align-paper-northeast")
        self.append_item(ALIGN_PAPER_SOUTHWEST, "align-paper-southwest")
        self.append_item(ALIGN_PAPER_SOUTH, "align-paper-south")
        self.append_item(ALIGN_PAPER_SOUTHEAST, "align-paper-southeast")
        self.append_item(ALIGN_PAPER_WEST, "align-paper-west")
        self.append_item(ALIGN_PAPER_CENTER_BOTH, "align-paper-center-both")
        self.append_item(ALIGN_PAPER_EAST, "align-paper-east")
        self.append_item(ALIGN_PAPER_CENTER_HORIZONTAL, "align-paper-center-horizontal")
        self.append_item(ALIGN_PAPER_CENTER_VERTICAL, "align-paper-center-vertical")
        self.ascend()

        self.append_menu("_" + _("Window"))
        self.append_item(gtk.STOCK_FULLSCREEN, "fullscreen", "<Control>F")

        self.append_menu("_" + _("Help"), right=True)
        self.append_item(gtk.STOCK_HELP, "help", "F1")
        self.append_separator()
        self.append_item(gtk.STOCK_ABOUT, "about")

        self.install_signals()
        self.show_all()
