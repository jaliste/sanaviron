#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A canvas for drawing things on it"""

import platform
import gtk

if platform.system() != 'Windows':
    gtk.threads_init()

import cairo
#import threads
import gobject

from holder import Holder, Property
from origin import Origin
from grid import Grid
from guides import Guides
from selection import Selection
from paper import Paper
from size import Size
from signalized import Signalized

from barcode import BarCode
from image import Image
from text import Text
from table import Table
from line import Line
from box import Box
from rounded import Rounded
from arc import Arc
from curve import Curve
from connector import Connector
from chart import Chart

from objects import *
from objects import opossite

import xml.parsers.expat

object = None

class BaseCanvas(Holder, gtk.Layout, Signalized):
    """This class represents a low level canvas"""

    def __init__(self):
        Holder.__init__(self)
        gtk.Layout.__init__(self)

        self.configure_handlers()
        
        self.set_can_default(True)
        self.set_can_focus(True)

        self.install_signal("select")
        self.install_signal("finalize")
        self.install_signal("edit-child")

    def configure_handlers(self):
        self.set_events(0)

        self.add_events(gtk.gdk.EXPOSURE_MASK)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.add_events(gtk.gdk.BUTTON_MOTION_MASK)
        #self.add_events(gtk.gdk.KEY_PRESS_MASK)

        #self.expose_id = self.connect("expose-event", self.expose)
        self.expose_id = self.connect("expose-event", self.expose)
        self.motion_id = self.connect("motion-notify-event", self.motion)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)
        #self.connect("key-press-event", self.key_press)
        
    #def key_press(self, widget, event):
    #    raise NotImplementedError
        
    def release(self, widget, event):
        raise NotImplementedError

    def motion(self, widget, event):
        raise NotImplementedError

    def press(self, widget, event):
        raise NotImplementedError

    def expose(self, widget, event):
        raise NotImplementedError
        
class Canvas(BaseCanvas):
    """This class represents a middle level canvas"""

    def __init__(self):
        BaseCanvas.__init__(self)
        self.origin = Origin()
        self.grid = Grid()
        self.guides = Guides()
        self.selection = Selection()
        self.gradients = list()
        self.children = list()
        self.pages = list()

        paper = Paper()
        self.total = Size()
        
        self.pages.append(paper)
        self.zoom = 1.0
        self.origin.x = 0 # XXX
        self.origin.y = 0 # XXX
        self.border = 25
        
        self.pick = False
        self.updated = False
        self.child = None
        self.stop_cursor_change = False


        self.horizontal_ruler = None
        self.vertical_ruler = None
        self.clipboard = None

        self.hints = False

    def debug(self, message):
        self.code_editor.editor.buffer.set_text(message)
      
    def release(self, widget, event):
        """
        This code is executed when you release the mouse button
        """
        if self.selection.active:
            self.unselect_all()
            for child in self.children:
                if child.in_selection(self.selection):
                    child.selected = True
                    self.emit("select", child)
                #elif child.resizing:
                #    child.resizing ^= 1
            self.selection.active = False
        else:
            for child in self.children:
                if child.selected:
                    self.emit("finalize", child)
                if child.resizing:
                    child.resizing ^= 1
                    child.direction = NONE
                    for control in child.handler.control:
                        control.pivot = False
                    self.emit("finalize", child)

        self.pick = False
        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))

        self.updated = False
        self.update()
        self.stop_cursor_change = False
        return True

    def motion(self, widget, event):
        """
        This code is executed when move the mouse pointer
        """
        self.disconnect(self.motion_id)
        self.horizontal_ruler.motion(self.horizontal_ruler, event, True)
        self.vertical_ruler.motion(self.vertical_ruler, event, True)
        x = event.x / self.zoom - self.origin.x
        y = event.y / self.zoom - self.origin.y

        if not self.stop_cursor_change:
            def get_direction_for_child_at_position(x, y, origin, children):
                for child in children:
                    if child.selected and child.at_position(x, y) and child.handler.at_position(x + origin.x, y + origin.y):
                            direction = child.handler.get_direction(x + origin.x, y + origin.y)
                            widget.bin_window.set_cursor(child.get_cursor(direction))
                            #child.direction = direction
                            return direction
                return NONE

            direction = get_direction_for_child_at_position(x, y, self.origin, self.children)

            if direction == NONE:
                if self.pick:
                    widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.PENCIL))
                else:
                    widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))

        if self.selection.active:
            self.selection.width = x - self.selection.x
            self.selection.height = y - self.selection.y
            self.updated = False
            self.update() # XXX
        elif event.state & gtk.gdk.BUTTON1_MASK:
            for child in self.children: # TODO
                if child.selected:
                    if child.resizing:
                        if not child.resize(x, y, self.grid):
                            x = self.grid.nearest(x)
                            y = self.grid.nearest(y)
                            child.transform(x, y)
                    else:
                        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                        child.move(x, y, self.grid)
                    self.emit("edit-child", child)
                    self.update()
        self.motion_id = self.connect("motion-notify-event", self.motion)
        return True

    def press(self, widget, event):
        """
        This code is executed when you press the mouse button
        """
        self.emit("focus", gtk.DIR_TAB_FORWARD)
        event.x = event.x / self.zoom - self.origin.x
        event.y = event.y / self.zoom - self.origin.y

        if self.pick:
            self.unselect_all()

            #x, y = self.get_pointer()
            child = self.child
            child.selected = True
            self.emit("select", child)
            child.resizing = True
            child.direction = SOUTHEAST
            child.x = self.grid.nearest(event.x)
            child.y = self.grid.nearest(event.y)
            child.pivot.x = child.x
            child.pivot.y = child.y
            child.width = 0
            child.height = 0
            self.add(child)
            #child.handler.control[child.direction].offset.x = event.x - child.x
            #child.handler.control[child.direction].offset.y = event.y - child.y
            widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER))
            self.stop_cursor_change = True
            return True

        selected = False
        move = False
        resizing = False
        self.unselect_all()
        for child in sorted(self.children, key=lambda child: child.z, reverse=True):
            if child.at_position(event.x, event.y):
                if child.selected:
                    move = True
                selected = True
                child.selected = True
                if child.handler.at_position(event.x + self.origin.x, event.y + self.origin.y):
                    child.resizing = True
                    child.direction = child.handler.get_direction(event.x + self.origin.x, event.y + self.origin.y)
                    for control in child.handler.control:
                        control.pivot = False
                    pivot = child.handler.control[opossite(child.direction)]
                    pivot.pivot = True
                    child.pivot.x = self.grid.nearest(pivot.x - self.origin.x)
                    child.pivot.y = self.grid.nearest(pivot.y - self.origin.x)
                    resizing = True
                    self.stop_cursor_change = True
                break

        if not resizing:
            for child in self.children:
                child.resizing = False
                if child.selected:
                    child.offset.x = event.x - child.x
                    child.offset.y = event.y - child.y
                    if (not child.at_position(event.x,
                        event.y) and not move and not event.state & gtk.gdk.CONTROL_MASK) or\
                       (child.at_position(event.x, event.y) and move and event.state & gtk.gdk.CONTROL_MASK):
                        child.selected = False
                    else:
                        child.selected = True
                        self.emit("select", child)

            if not selected and not move:
                self.selection.x = event.x
                self.selection.y = event.y
                self.selection.width = 0
                self.selection.height = 0
                self.selection.active = True
                widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
            else:
                self.updated = False
            self.update() # XXX
            self.stop_cursor_change = True

        return True

    def expose(self, widget, event):
        self.disconnect(self.expose_id)
        context = widget.bin_window.cairo_create()
        context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        context.clip()
        context.scale(self.zoom, self.zoom)
        self.total.width = int(self.pages[0].width * self.zoom + 2 * self.border)
        self.total.height = int(len(self.pages) * self.pages[0].height * self.zoom +
                                (len(self.pages) + 1) * self.border)
        self.set_size_request(self.total.width, self.total.height)
        context.set_source_rgb(0.55, 0.55, 0.55) #background
        context.paint()

        for i, page in enumerate(self.pages):
            page.y = i * page.height + self.border * (i + 1) / self.zoom
            page.x = self.border / self.zoom

            page.draw(context)

            self.origin.x = page.x + page.left # + self.border
            self.origin.y = page.y + page.top # + self.border

            if self.grid.active:
                self.grid.x = self.origin.x
                self.grid.y = self.origin.y
                self.grid.width = page.width - page.left - page.right
                self.grid.height = page.height - page.top - page.bottom
                self.grid.draw(context)

            if self.guides.active:
                self.guides.x = self.origin.x
                self.guides.y = self.origin.y
                self.guides.width = page.width - page.left - page.right
                self.guides.height = page.height - page.top - page.bottom
                self.guides.draw(context)

        for child in sorted(self.children, key=lambda child: child.z):
            child.x += self.origin.x
            child.y += self.origin.y
            child.hints = self.hints # TODO Not here
            child.draw(context)
            child.x -= self.origin.x
            child.y -= self.origin.y

        if self.selection.active:
            self.selection.x += self.origin.x
            self.selection.y += self.origin.y
            self.selection.draw(context)
            self.selection.x -= self.origin.x
            self.selection.y -= self.origin.y
        self.updated = True
        self.expose_id = self.connect("expose-event", self.expose)
        return True

    add = lambda self, child: self.children.append(child)

    #update = lambda self: self.queue_draw()
    def update(self):
        if not self.updated:
            pass
        self.queue_draw()

class ExtendedCanvas(Canvas):
    """This class represents a high level canvas"""

    def __init__(self):
        Canvas.__init__(self)

    def add_page(self):
        page = self.pages[0]
        self.pages.append(page)
        self.queue_draw()

    def set_scale_absolute(self, scale):
        self.zoom = scale
        self.queue_draw()

    def set_scale_factor(self, factor):
        self.zoom += factor
        if self.zoom < 0.05:
            self.zoom = 0.05
        self.queue_draw()

    zoom_out = lambda self, factor=-0.05: self.set_scale_factor(factor)

    zoom_in = lambda self, factor=0.05: self.set_scale_factor(factor)

    zoom_normal = lambda self: self.set_scale_absolute(1.0)

    def create(self, child):
        self.stop_cursor_change = False
        self.pick = True
        self.child = child
        child.z = len(self.children)
        #child.connect("changed", self.update, child)

    def cut(self, *args):
        self.copy()
        self.delete()

    def copy(self, *args):
        self.clipboard = '<clipboard>'
        for child in self.children:
            if child.selected:
                self.clipboard += child.serialize()
        self.clipboard += '</clipboard>'

    def paste(self, *args):
        self.unserialize(self.clipboard)
        self.unselect_all(False)
        self.select_last()
        # Select last

    def delete(self, *args):
        restart = True # i don't remember why use this
        while restart:
            restart = False
            for child in self.children:
                if child.selected:
                    self.children.remove(child)
                    restart = True
                    break
        self.update()

    def select_all(self, *args):
        for child in self.children:
            child.selected = True
        self.queue_draw()

    def unselect_all(self, update=True, *args):
        for child in self.children:
            child.selected = False
        if update:
            self.update()

    def select_last(self, *args):
        self.children[len(self.children) - 1].selected = True
        self.update()

    def bring_to_back(self, *args):
        for child in self.children:
            if child.selected:
                child.z -= 1
            else:
                child.z += 1
        self.update()

    def bring_to_front(self, *args):
        for child in self.children:
            if child.selected:
                child.z += 1
            else:
                child.z -= 1
        self.update()

    def remove_split(self, *args):
        for child in self.children:
            if child.selected and child.__name__ == 'Box':
                child.remove_separator()
        self.update()

    def split_vertically(self, *args):
        for child in self.children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_vertical(child.width / 2)
        self.update()

    def split_horizontally(self, *args):
        for child in self.children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_horizontal(child.height / 2)
        self.update()

    def paper_center_horizontal(self, *args):
        for child in self.children:
            if child.selected:
                child.x = int((self.pages[0].width - child.width) / 2 - self.border)
        self.update()

    def get_first_page(self):
        return self.pages[0]

    def draw_children(self, page, context): # XXX
        for child in self.children:
            selected = child.selected
            child.selected = False
            child.x += page.left
            child.y += page.top
            child.draw(context)
            child.x -= page.left
            child.y -= page.top
            child.selected = selected

    def toggle_snap(self, *args):
        self.grid.snap ^= 1

    def toggle_grid(self, *args):
        self.grid.active ^= 1
        self.update()

    def toggle_guides(self, *args):
        self.guides.active ^= 1
        self.update()

    def toggle_margins(self, *args):
        for page in self.pages:
            page.active ^= 1
        self.update()

    def toggle_hints(self, *args):
        self.hints ^= 1
        self.update()

    def get_filename(self, filename, extension):
        if not filename.endswith("." + extension):
            return filename + "." + extension
        else:
            return filename

    def save_to_pdf(self, filename):
        filename = self.get_filename(filename, "pdf")
        for i, page in enumerate(self.pages):
            surface = cairo.PDFSurface(filename, self.pages[i].width, self.pages[i].height)
            context = cairo.Context(surface)
            self.draw_children(page, context)
            #context.show_page()
            surface.flush()

    def save_to_png(self, filename):
        filename = self.get_filename(filename, "png")
        # TODO: Multiple pages
        page = self.get_first_page()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, page.width, page.height)
        context = cairo.Context(surface)
        self.draw_children(page, context)
        context.show_page()
        #surface.flush()

    def save_to_postscript(self, filename):
        pass # TODO

    def save_to_xml(self, filename):
        filename = self.get_filename(filename, "xml")
        document = self.serialize()
        handle = open(filename, 'w')
        handle.write(document)
        handle.close()

    def load_from_xml(self, filename):
        handle = open(filename)
        document = handle.read()
        handle.close()
        self.unserialize(document)

    def unserialize(self, document):
        def element_start(name, attributes):
            global object

            if name == "object":
                type = attributes["type"]
                code = "%s()" % type
                object = eval(code)
            elif name == "property":
                attribute = attributes["name"]
                try:
                    type = attributes["type"]
                except:
                    type = "AUTOMATIC"
                value = attributes["value"]
                property = Property(attribute, value, type)
                object.set_property(attribute, value, type)

        def element_end(name):
            if name == "object":
                self.add(object)

        #def element_body(data):
        #  print "data:", repr(data)

        parser = xml.parsers.expat.ParserCreate()

        parser.StartElementHandler = element_start
        parser.EndElementHandler = element_end
        #parser.CharacterDataHandler = element_body

        parser.Parse(document, 1)

        self.update()

    def serialize(self):
        text = "<document page=\"1\">\n"
        for child in self.children:
            text += child.serialize()
        text += "</document>\n"
        return text
        
class TestingCanvas(ExtendedCanvas):
    """This class represents a testing canvas"""

    def __init__(self):
        ExtendedCanvas.__init__(self)

        print _("WARNING: You are using a testing canvas.")
