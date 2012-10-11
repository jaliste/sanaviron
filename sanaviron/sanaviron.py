#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(__file__))
import platform
import gtk
import cairo
#default_settings = gtk.settings_get_default()
#default_screen_settings = gtk.settings_get_for_screen(gtk.gdk.screen_get_default())

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
from objects.barcode import BarCode
from objects.box import Box
from objects.chart import Chart
from objects.curve import Curve
from objects.connector import Connector
from objects.image import Image
from objects.line import Line
from objects.rounded import Rounded
from objects.table import Table
from objects.text import Text

from objects.shape import Shape

from ui.menu import Menu
from ui.toolbars import HorizontalToolbar, VerticalToolbar
from ui.editor import Editor
from ui.statusbar import Statusbar
from ui import INFORMATION

setup = gtk.PageSetup()
settings = gtk.PrintSettings()

APP_VERSION = open(os.path.join(os.path.dirname(__file__),  "..", "VERSION")).read()

DEBUG = False

class Application(gtk.Window):
    """This class represents an application"""
    application = None

    def __new__(self, *args, **kwargs):
        if self.application:
            return self.application
        else:
            self.application = super(Application, self).__new__(self)
            self.application.initialize()
            return self.application

    def initialize(self):
        gtk.Window.__init__(self)
        self.set_size_request(640, 480)
        if '--debug' in sys.argv:
            self.set_default_size(1366, 768)
        else:
            self.set_default_size(800, 600)
        self.winstate = 0
        self.maximize()
        self.connect("delete-event", self.quit)

        self.filename = None
        self.update_title()

        icon = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__), "images", "canvas-logo.png"))
        self.set_icon(icon)

        vbox = gtk.VBox()
        self.add(vbox)

        self.menu = Menu()
        vbox.pack_start(self.menu, False, False)

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

        def get_source_view():
            source = gtk.ScrolledWindow()
            source.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

            view = gtk.TextView()
            self.code = gtk.TextBuffer()
            view.set_buffer(self.code)
            source.add(view)

            return source

        if '--source-editor-test' in sys.argv:
            while True:
                try:
                    from ui.code_editor import SourcePad
                except:
                    source = get_source_view()
                    break

                source = SourcePad()
                self.code = source.buffer
                source.set_language("xml")
                break
        else:
            source = get_source_view()

        notebook.append_page(source, label)

        self.menu.connect("new", self.new)
        self.menu.connect("open", self.open)
        self.menu.connect("save", self.save)
        self.menu.connect("save-as", self.save_as)
        self.menu.connect("page-setup", self.page_setup)
        self.menu.connect("export-to-pdf", self.export_to_pdf)
        self.menu.connect("quit", self.quit)

        self.menu.connect("cut", self.editor.canvas.cut)
        self.menu.connect("copy", self.editor.canvas.copy)
        self.menu.connect("paste", self.editor.canvas.paste)
        self.menu.connect("delete", self.editor.canvas.delete)
        self.menu.connect("select-all", self.editor.canvas.select_all)

        self.menu.connect("margins", self.editor.canvas.toggle_margins)
        self.menu.connect("grid", self.editor.canvas.toggle_grid)
        self.menu.connect("guides", self.editor.canvas.toggle_guides)
        self.menu.connect("snap", self.editor.canvas.toggle_snap)
        self.menu.connect("hints", self.editor.canvas.toggle_hints)
        self.menu.connect("properties", self.editor.toggle_properties)
        self.menu.connect("menubar", self.toggle_menubar)
        self.menu.connect("statusbar", self.toggle_statusbar)

        self.menu.connect("bring-to-front", self.editor.canvas.bring_to_front)
        self.menu.connect("bring-to-back", self.editor.canvas.bring_to_back)

        self.menu.connect("align-paper-center-horizontal", self.editor.canvas.paper_center_horizontal)

        self.menu.connect("line", self.create, "Line")
        self.menu.connect("curve", self.create, "Curve")
        self.menu.connect("connector", self.create, "Connector")
        self.menu.connect("box", self.create, "Box")
        self.menu.connect("rounded-box", self.create, "Rounded")
        self.menu.connect("text", self.create, "Text")
        self.menu.connect("barcode", self.create, "BarCode")
        self.menu.connect("table", self.create, "Table")
        self.menu.connect("image", self.create, "Image")
        self.menu.connect("chart", self.create, "Chart")

        self.menu.connect("fullscreen", self.fullscreen)
        self.menu.connect("about", self.about)
        self.menu.connect("help", self.help)

        self.menu.connect("split-horizontally", self.editor.canvas.split_horizontally)
        self.menu.connect("split-vertically", self.editor.canvas.split_vertically)
        self.menu.connect("remove-split", self.editor.canvas.remove_split)

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

        vtoolbar.connect("line", self.create, "Line")
        vtoolbar.connect("arc", self.create, "Arc")
        vtoolbar.connect("curve", self.create, "Curve")
        vtoolbar.connect("connector", self.create, "Connector")
        vtoolbar.connect("box", self.create, "Box")
        vtoolbar.connect("rounded-box", self.create, "Rounded")
        vtoolbar.connect("text", self.create, "Text")
        vtoolbar.connect("barcode", self.create, "BarCode")
        vtoolbar.connect("table", self.create, "Table")
        vtoolbar.connect("image", self.create, "Image")
        vtoolbar.connect("chart", self.create, "Chart")

        vtoolbar.connect("split-horizontally", self.editor.canvas.split_horizontally)
        vtoolbar.connect("split-vertically", self.editor.canvas.split_vertically)
        vtoolbar.connect("remove-split", self.editor.canvas.remove_split)

        notebook.connect("switch-page", self.switch)

        self.connect("key-press-event", self.key_press)

    def run(self):
       self.show_all()
       gtk.main()

    def update_title(self):
        document = self.filename if self.filename else _("New document")
        title = _("%(document)s - Sanaviron %(version)s") % {"document": document, "version": APP_VERSION}
        self.set_title(title)

    def switch(self, widget, child, page):
        document = self.editor.canvas.serialize()
        self.code.set_text(document)

    def key_handler(self, keyname):
        if keyname == "<Control><Shift>V":
            self.editor.canvas.add_box_separator_vertical()
        if keyname == "<Control><Shift>H":
            self.editor.canvas.add_box_separator_horizontal()
        if keyname == "<Control><Shift>Escape":
            self.toggle_menubar()
        if keyname in ["<Control><Shift>Colon", "<Control><Shift>Period"]:
            self.editor.canvas.hints ^= 1
            self.editor.canvas.update()

    def key_press(self, widget, event):
        keyval = event.keyval
        keyname = gtk.gdk.keyval_name(keyval)
        if keyname.startswith('Control') or\
           keyname.startswith('Shift') or\
           keyname.startswith('Alt'):
            return False
        keyname = keyname.capitalize()
        if event.state & gtk.gdk.SHIFT_MASK:
            keyname = "<Shift>%s" % keyname
        if event.state & gtk.gdk.CONTROL_MASK:
            keyname = "<Control>%s" % keyname
        self.key_handler(keyname)
        return False

    def toggle_menubar(self, *args):
        if self.menu.get_visible():
            self.menu.hide()
            self.editor.notification.notificate(_("Press <i><b>Control+Shift+Escape</b></i> to show again."), INFORMATION)
        else:
            self.menu.show()

    def toggle_statusbar(self, *args):
        if self.status.get_visible():
            self.status.hide()
        else:
            self.status.show()

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
            self.filename = filename
            if filename is not None:
                self.editor.canvas.load_from_xml(filename)
                self.update_title()

        dialog.destroy()

    def save(self, widget, data):
        if not self.filename:
            return
        current = self.editor.canvas.serialize()
        original = open(self.filename).read()
        print original
        print current
        if original == current:
            return
        print "saving"
        #self.editor.canvas.save_to_xml(self.filename)

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
            self.filename = filename
            if filename is not None:
                self.editor.canvas.save_to_xml(filename)
                self.update_title()

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
        print "Motion events:", self.editor.canvas.statics.motion
        print "Expose events:", self.editor.canvas.statics.expose
        print "Consumed motion events:", self.editor.canvas.statics.consumed.motion
        print("Bye ;-)")
        gtk.main_quit()
        return True

    create = lambda self, widget, data, name: self.editor.canvas.create(Shape(name))

    def help(self, widget, data):
        cwd = os.getcwd()
        language = os.environ['LANG'].split('_')[0]
        if not language or language == 'C':
            language = "es"
        url = 'file://%s/../doc/help/%s/index.html' % (cwd, language)
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
        dialog.set_website("http://www.sanaviron.org/")
        dialog.set_website_label(_("Official site"))
        dialog.set_license(open(os.path.join(os.path.dirname(__file__),  "..", "COPYING")).read())
        dialog.set_wrap_license(False)
        dialog.set_authors(["Juan Manuel Mouriz <jmouriz@sanaviron.org>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_documenters([_("Undocumented yet :'(")])
        dialog.set_artists(["Juan Manuel Mouriz <jmouriz@sanaviron.org>", "Ivlev Denis <ivlevdenis.ru@gmail.com>"])
        dialog.set_translator_credits("Juan Manuel Mouriz <jmouriz@sanaviron.org> " + _(
            "(Spanish)") + "\n" + "Ivlev Denis <ivlevdenis.ru@gmail.com> " + _("(Russian)"))
        logo = gtk.gdk.pixbuf_new_from_file(os.path.join(os.path.dirname(__file__), "images", "canvas-logo.png"))
        dialog.set_logo(logo)
        #dialog.set_logo_icon_name(self.icon_name)
        dialog.run()
        dialog.destroy()


def startapp():
    if '--debug' in sys.argv:
        import gc
        #gc.enable()
        #gc.set_debug(gc.DEBUG_LEAK)
        #gc.set_debug(gc.DEBUG_OBJECTS)
        global DEBUG
        DEBUG = True

    print "Sanaviron version:", APP_VERSION
    print "System:", platform.system(), platform.release(), platform.version()
    print "Python version:", platform.python_version()
    print "GTK version:", '.'.join(map(str, gtk.ver))
    print "Cairo version:", cairo.cairo_version_string()

    application = Application()

    # Singleton test
    instance = Application()
    print application, "==", instance
    assert 1 is 1 and 1 == 1 and application is instance and application == instance
    print application.editor.canvas
    print instance.editor.canvas

    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("..", "examples", "invoice.xml"))

    application.run()

if __name__ == '__main__':
    startapp()
