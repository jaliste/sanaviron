#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(__file__))
import platform
import gtk
import cairo

if platform.system() != 'Windows':
    gtk.threads_init()
else:
    import locale
    import os
    if os.getenv('LANG') is None:
        language, encoding = locale.getdefaultlocale()
        os.environ['LANG'] = language

import gettext
TRANSLATION_DOMAIN = "test"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "localization")
gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

from objects.arc import Arc
from objects.barcode import BARCODE_39
from objects.barcode import BarCode
from objects.box import Box
from objects.bubble import Bubble
from objects.chart import Chart
from objects.curve import Curve
from objects.connector import Connector
from objects.image import Image
from objects.line import Line
from objects.rounded import Rounded
from objects.table import Table
from objects.text import Text

from ui.menu import Menu
from ui.toolbars import HorizontalToolbar, VerticalToolbar
#from ui.browser import Browser
from ui.editor import Editor
from ui.statusbar import Statusbar

setup = gtk.PageSetup()
settings = gtk.PrintSettings()

APP_VERSION = "0.1.0"

DEBUG = False

class Application(gtk.Window):
    """This class represents an application"""

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title(_("Document designer"))
        self.set_size_request(640, 480)
        self.set_default_size(800, 600)
        self.winstate = 0
        self.maximize()
        self.connect("delete-event", self.quit)

        icon = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__), "images", "canvas-logo.png"))
        self.set_icon(icon)

        vbox = gtk.VBox()
        self.add(vbox)

        menu = Menu()
        vbox.pack_start(menu, False, False)

        htoolbar = HorizontalToolbar()
        vbox.pack_start(htoolbar, False, False)

        hbox = gtk.HBox()
        vbox.add(hbox)

        vtoolbar = VerticalToolbar()
        hbox.pack_start(vtoolbar, False, False)

        notebook = gtk.Notebook()
        notebook.set_show_tabs(DEBUG)
        notebook.set_show_border(False)
        #notebook.set_tab_pos(gtk.POS_LEFT)
        notebook.set_tab_pos(gtk.POS_RIGHT)
        hbox.add(notebook)

        self.status = Statusbar()
        self.id = self.status.get_context_id(_("Edit mode"))
        vbox.pack_start(self.status, False, False)

        label = gtk.Label(_("Design view"))
        label.set_angle(90)

        self.editor = Editor()
        self.editor.set_paper()
        notebook.append_page(self.editor, label)

        label = gtk.Label(_("XML view"))
        label.set_angle(90)

        area = gtk.ScrolledWindow()
        area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        notebook.append_page(area, label)

        view = gtk.TextView()
        self.code = gtk.TextBuffer()
        view.set_buffer(self.code)
        area.add(view)

        menu.connect("new", self.new)
        menu.connect("open", self.open)
        menu.connect("save", self.save)
        menu.connect("save-as", self.save_as)
        menu.connect("page-setup", self.page_setup)
        menu.connect("export-to-pdf", self.export_to_pdf)
        menu.connect("quit", self.quit)

        menu.connect("cut", self.editor.canvas.cut)
        menu.connect("copy", self.editor.canvas.copy)
        menu.connect("paste", self.editor.canvas.paste)
        menu.connect("delete", self.editor.canvas.delete)
        menu.connect("select-all", self.editor.canvas.select_all)

        menu.connect("bring-to-front", self.editor.canvas.bring_to_front)
        menu.connect("bring-to-back", self.editor.canvas.bring_to_back)

        menu.connect("paper-center-horizontal", self.editor.canvas.paper_center_horizontal)
        
        menu.connect("line", self.line)
        menu.connect("curve", self.curve)
        menu.connect("connector", self.connector)
        menu.connect("box", self.box)
        menu.connect("rounded-box", self.rounded_box)
        menu.connect("bubble", self.bubble)
        menu.connect("text", self.text)
        menu.connect("barcode", self.table)
        menu.connect("table", self.barcode)
        menu.connect("chart", self.chart)
        menu.connect("fullscreen", self.fullscreen)
        menu.connect("about", self.about)
        menu.connect("help", self.help)

        htoolbar.connect("new", self.new)
        htoolbar.connect("open", self.open)
        htoolbar.connect("save", self.save)
        htoolbar.connect("snap", self.editor.canvas.toggle_snap)
        htoolbar.connect("grid", self.editor.canvas.toggle_grid)
        htoolbar.connect("guides", self.editor.canvas.toggle_guides)
        htoolbar.connect("margins", self.editor.canvas.toggle_margins)
        htoolbar.connect("cut", self.editor.canvas.cut)
        htoolbar.connect("copy", self.editor.canvas.copy)
        htoolbar.connect("paste", self.editor.canvas.paste)
        htoolbar.connect("delete", self.editor.canvas.delete)
        htoolbar.connect("bring-to-front", self.editor.canvas.bring_to_front)
        htoolbar.connect("bring-to-back", self.editor.canvas.bring_to_back)
        htoolbar.connect("export-to-pdf", self.export_to_pdf)
        htoolbar.connect("help", self.help)

        vtoolbar.connect("line", self.line)
        vtoolbar.connect("arc", self.arc)
        vtoolbar.connect("curve", self.curve)
        vtoolbar.connect("connector", self.connector)
        vtoolbar.connect("box", self.box)
        vtoolbar.connect("rounded-box", self.rounded_box)
        vtoolbar.connect("bubble", self.bubble)
        vtoolbar.connect("text", self.text)
        vtoolbar.connect("barcode", self.barcode)
        vtoolbar.connect("table", self.table)
        vtoolbar.connect("chart", self.chart)
        vtoolbar.connect("image", self.image)

        notebook.connect("switch-page", self.switch)

        self.connect("key-press-event", self.key_press)
        
    def run(self):
       self.show_all()
       gtk.main()

    def switch(self, widget, child, page):
        document = self.editor.canvas.serialize()
        self.code.set_text(document)

    def key_handler(self, keyname):
        if keyname == "<Control><Shift>V":
            self.editor.canvas.add_box_separator_vertical()
        if keyname == "<Control><Shift>H":
            self.editor.canvas.add_box_separator_horizontal()

    def key_press(self, widget, event):
        keyval = event.keyval
        keyname = gtk.gdk.keyval_name (keyval)
        if keyname.startswith('Control') or\
           keyname.startswith('Shift') or\
           keyname.startswith('Alt') or\
           keyname.startswith('Meta'):
            return False
        keyname = keyname.upper()
        if event.state & gtk.gdk.SHIFT_MASK:
            keyname = "<Shift>%s" % keyname
        if event.state & gtk.gdk.CONTROL_MASK:
            keyname = "<Control>%s" % keyname
        print "%s has pressed" % keyname
        self.key_handler(keyname)
        return False

    def new(self, widget, data):
        self.editor.canvas.children = list()
        self.editor.canvas.queue_draw()

    def open(self, widget, data):
        # XXX funcional
        dialog = gtk.FileChooserDialog(title=_("Open document"),
            parent=self,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT),
            backend=None)

        dialog.set_transient_for(self)
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name(_("XML files"))
        filter.add_mime_type("document/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == gtk.RESPONSE_ACCEPT:
            filename = dialog.get_filename()
            if filename is not None:
                self.editor.canvas.load_from_xml(filename)

        dialog.destroy()

    def save(self, widget, data):
        pass
    #    self.editor.canvas.save_to_xml()

    def save_as(self, widget, data):
        dialog = gtk.FileChooserDialog(title=_("Save document as"),
            parent=self,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT),
            backend=None)

        dialog.set_transient_for(self)
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)

        filter = gtk.FileFilter()
        filter.set_name(_("XML files"))
        filter.add_mime_type("document/xml")
        filter.add_pattern("*.xml")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == gtk.RESPONSE_ACCEPT:
            filename = dialog.get_filename()
            if filename is not None:
                self.editor.canvas.save_to_xml(filename)

        dialog.destroy()

    def page_setup(self, widget, data):
        global setup, settings
        setup.settings = settings
        setup = gtk.print_run_page_setup_dialog(self, setup, settings)

        size = setup.get_paper_size()
        orientation = setup.get_orientation()

        # TODO canvas->margins
        for page in self.editor.canvas.pages:
            page.top = setup.get_top_margin(gtk.UNIT_POINTS)
            page.left = setup.get_left_margin(gtk.UNIT_POINTS)
            page.bottom = setup.get_bottom_margin(gtk.UNIT_POINTS)
            page.right = setup.get_right_margin(gtk.UNIT_POINTS)

        width = size.get_width(gtk.UNIT_POINTS)
        height = size.get_height(gtk.UNIT_POINTS)

        # no int
        if orientation in (gtk.PAGE_ORIENTATION_PORTRAIT, gtk.PAGE_ORIENTATION_REVERSE_PORTRAIT):
            orientation = _("Vertical")
            width = int(width)
            height = int(height)
        else:
            orientation = _("Landscape")
            saved_height = height
            height = int(width)
            width = int(saved_height)

        # TODO: canvas->page_size
        for page in self.editor.canvas.pages:
            page.width = width
            page.height = height

        name = size.get_display_name()
        text = "%s %s (%d dots x %d dots)" % (name, orientation, width, height)
        self.status.push(self.id, text)
        self.editor.canvas.queue_draw()

    def export_to_pdf(self, widget, format):
        dialog = gtk.FileChooserDialog(title=_("Save PDF file as"),
            parent=self,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT),
            backend=None)

        dialog.set_transient_for(self)
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)

        filter = gtk.FileFilter()
        filter.set_name(_("PDF files"))
        filter.add_mime_type("document/pdf")
        filter.add_pattern("*.pdf")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            filename = dialog.get_filename()
            if filename is not None:
                self.editor.canvas.save_to_pdf(filename)

        dialog.destroy()

    def fullscreen(self, widget, data):
        if not self.winstate:
            self.winstate = not self.winstate
            self.window.fullscreen()
        else:
            self.window.unfullscreen()

    def quit(self, widget, event):
        gtk.main_quit()
        print("Bye ;-)")
        return True

    def line(self, widget, data):
        self.editor.canvas.create(Line())

    def arc(self, widget, data):
        self.editor.canvas.create(Arc())

    def curve(self, widget, data):
        self.editor.canvas.create(Curve())

    def connector(self, widget, data):
        self.editor.canvas.create(Connector())

    def box(self, widget, data):
        self.editor.canvas.create(Box())

    def rounded_box(self, widget, data):
        self.editor.canvas.create(Rounded())

    def bubble(self, widget, data):
        self.editor.canvas.create(Bubble())

    def text(self, widget, data):
        child = Text(_("Insert text here"))
        child.set_property("size", 12)
        self.editor.canvas.create(child)

    def image(self, widget, data):
        self.editor.canvas.create(Image(os.path.join("images", "canvas-logo.png")))

    def barcode(self, widget, data):
        self.editor.canvas.create(BarCode("800894002700", BARCODE_39))

    def table(self, widget, data):
        self.editor.canvas.create(Table(5, "0", _("Column 1")))

    def chart(self, widget, data):
        self.editor.canvas.create(Chart())

    def help(self, widget, data):
        cwd = os.getcwd()
        url = "file://" + cwd + "/help/index.html"
        import webbrowser

        webbrowser.open_new(url)

    def about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_transient_for(self)
        dialog.set_program_name("sanaviron")
        dialog.set_name("sanaviron")
        dialog.set_version(APP_VERSION)
        dialog.set_copyright("Copyright 2012 - Juan Manuel Mouriz, Ivlev Denis")
        dialog.set_comments(_(
            "A program to design reports, invoices, documents, labels and more. Based on the 2D drawing engine \"sanaviron\"."))
        dialog.set_website("http://code.google.com/p/sanaviron/")
        dialog.set_website_label(_("Unofficial project site at Google"))
        dialog.set_license(open(os.path.join(os.path.dirname(__file__, "..", "COPYING"))).read())
        dialog.set_wrap_license(False)
        dialog.set_authors(["Juan Manuel Mouriz <jmouriz@gmail.com>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_documenters([_("Undocumented yet :'(")])
        dialog.set_artists(["Juan Manuel Mouriz <jmouriz@gmail.com>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_translator_credits("Juan Manuel Mouriz <jmouriz@gmail.com> " + _(
            "(Spanish)") + "\n" + "Ivlev Denis <ivlevdenis.ru@gmail.com> " + _("(Russian)"))
        logo = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__), "images", "canvas-logo.png"))
        dialog.set_logo(logo)
        #dialog.set_logo_icon_name(self.icon_name)
        dialog.run()
        dialog.destroy()


def startapp():
    if '--debug' in sys.argv:
        import gc
        gc.enable()
        gc.set_debug(gc.DEBUG_LEAK)
        global DEBUG
        DEBUG = True

    print "Sanaviron version:", APP_VERSION
    print "System:", platform.system(), platform.release(), platform.version()
    print "Python version:", platform.python_version()
    print "GTK version:", '.'.join(map(str, gtk.ver))
    print "Cairo version:", cairo.cairo_version_string()

    application = Application()
    
    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("examples", "invoice.xml"))
    
    application.run()

if __name__ == '__main__':
    startapp()
