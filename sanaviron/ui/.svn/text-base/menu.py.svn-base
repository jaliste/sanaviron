#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
import gobject
from ui.stock import *

class Menu(gtk.VBox):
    """This class represents a pulldown menubar"""

    def __init__(self):
        gtk.VBox.__init__(self)
        self.connect("realize", self.realize)

        gobject.signal_new("new", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("open", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("save", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("save-as", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("page-setup", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("print", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("export-to-pdf", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("quit", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("fullscreen", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("help", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("about", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("copy", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("cut", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("paste", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("delete", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("select-all", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("bring-to-front", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("bring-to-back", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("paper-center-horizontal", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

        gobject.signal_new("line", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("arc", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("curve", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("connector", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("box", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("rounded-box", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("bubble", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("text", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("barcode", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("table", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("chart", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("image", Menu, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

    def realize(self, widget):
        bindings = gtk.AccelGroup()

        toplevel = self.get_toplevel()
        toplevel.add_accel_group(bindings)
        
        bar = gtk.MenuBar()
        self.add(bar)

        menuitem = gtk.MenuItem("_" + _("File"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_NEW)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "new")
        key, mask = gtk.accelerator_parse("<Control>N")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "open")
        key, mask = gtk.accelerator_parse("<Control>O")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_SAVE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "save")
        key, mask = gtk.accelerator_parse("<Control>S")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "save-as")
        key, mask = gtk.accelerator_parse("<Control><Shift>S")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_PAGE_SETUP)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "page-setup")

        menuitem = gtk.ImageMenuItem(gtk.STOCK_PRINT_PREVIEW)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "print-preview")
        key, mask = gtk.accelerator_parse("<Control><Shift>P")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_PRINT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "print")
        key, mask = gtk.accelerator_parse("<Control>P")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.MenuItem("_" + _("Export"))
        menu.append(menuitem)
        submenu = gtk.Menu()
        menuitem.set_submenu(submenu)

        menuitem = gtk.ImageMenuItem(EXPORT_TO_PDF)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "export-to-pdf")

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "quit")
        key, mask = gtk.accelerator_parse("<Control>Q")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.MenuItem(_("Edit"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_UNDO)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "undo")
        key, mask = gtk.accelerator_parse("<Control>Z")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_REDO)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "redo")
        key, mask = gtk.accelerator_parse("<Control>Y")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_COPY)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "copy")
        key, mask = gtk.accelerator_parse("<Control>C")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_CUT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "cut")
        key, mask = gtk.accelerator_parse("<Control>X")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_PASTE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "paste")
        key, mask = gtk.accelerator_parse("<Control>V")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_DELETE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "delete")
        key, mask = gtk.accelerator_parse("Delete")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_SELECT_ALL)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "select-all")
        key, mask = gtk.accelerator_parse("<Control>A")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.MenuItem(_("Insert"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(LINE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "line")

        menuitem = gtk.ImageMenuItem(ARC)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "arc")

        menuitem = gtk.ImageMenuItem(CURVE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "curve")

        menuitem = gtk.ImageMenuItem(CONNECTOR)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "connector")

        menuitem = gtk.ImageMenuItem(BOX)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "box")

        menuitem = gtk.ImageMenuItem(ROUNDED_BOX)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "rounded-box")

        menuitem = gtk.ImageMenuItem(BUBBLE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "bubble")

        menuitem = gtk.ImageMenuItem(TEXT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "text")

        menuitem = gtk.ImageMenuItem(TABLE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "barcode")

        menuitem = gtk.ImageMenuItem(CHART)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "chart")

        menuitem = gtk.ImageMenuItem(BARCODE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "table")

        menuitem = gtk.ImageMenuItem(IMAGE)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "image")

        menuitem = gtk.MenuItem(_("Format"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_SELECT_FONT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "select-font")

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_SELECT_COLOR)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "select-color")

        menuitem = gtk.MenuItem(_("Tools"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(GROUP)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "group")
        key, mask = gtk.accelerator_parse("<Control>G")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(UNGROUP)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "ungroup")
        key, mask = gtk.accelerator_parse("<Control><Shift>G")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(BRING_TO_FRONT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "bring-to-front")
        key, mask = gtk.accelerator_parse("<Control>plus")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(BRING_TO_BACK)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "bring-to-back")
        key, mask = gtk.accelerator_parse("<Control>minus")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_FIT)
        menu.append(menuitem)
        submenu = gtk.Menu()
        menuitem.set_submenu(submenu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_FIT)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "zoom-fit")
        key, mask = gtk.accelerator_parse("<Control>0")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_100)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "zoom-100")
        key, mask = gtk.accelerator_parse("<Control>1")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_IN)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "zoom-in")
        key, mask = gtk.accelerator_parse("<Control><Shift>plus")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ZOOM_OUT)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "zoom-out")
        key, mask = gtk.accelerator_parse("<Control><Shift>minus")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_BOTH) # TODO
        menu.append(menuitem)
        submenu = gtk.Menu()
        menuitem.set_submenu(submenu)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTHWEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_NORTHEAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTHWEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_SOUTHEAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_WEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_BOTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_EAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_HORIZONTAL)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_OBJECTS_CENTER_VERTICAL)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_BOTH) # TODO
        menu.append(menuitem)
        submenu = gtk.Menu()
        menuitem.set_submenu(submenu)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTHWEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_NORTHEAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTHWEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_SOUTHEAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_WEST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_BOTH)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_EAST)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_HORIZONTAL)
        submenu.append(menuitem)
        menuitem.connect("activate", self.activate, "paper-center-horizontal")

        menuitem = gtk.ImageMenuItem(ALIGN_PAPER_CENTER_VERTICAL)
        submenu.append(menuitem)
        #menuitem.connect("activate", gtk.main_quit)

        menuitem = gtk.MenuItem(_("Window"))
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_FULLSCREEN)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "fullscreen")
        key, mask = gtk.accelerator_parse("<Control>F")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        menuitem = gtk.MenuItem(_("Help"))
        menuitem.set_right_justified(True)
        bar.append(menuitem)
        menu = gtk.Menu()
        menuitem.set_submenu(menu)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_HELP)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "help")
        key, mask = gtk.accelerator_parse("F1")
        menuitem.add_accelerator("activate", bindings, key, mask, gtk.ACCEL_VISIBLE)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        menuitem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu.append(menuitem)
        menuitem.connect("activate", self.activate, "about")

        bar.show_all()

    def activate(self, widget, data):
        print data
        self.emit(data, None)
