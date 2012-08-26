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

from holder import Holder
from origin import Origin
from grid import Grid
from guides import Guides
from selection import Selection
from paper import Paper
from size import Size

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
from bubble import Bubble

from objects import *

import xml.parsers.expat

object = None

class BaseCanvas(Holder, gtk.Layout): ### LOW-LEVEL CODE HERE
    """This class represents a canvas"""

    def __init__(self):
        Holder.__init__(self)
        gtk.Layout.__init__(self)
        
        self.install_signals()
        self.configure_handlers()
        
        self.set_can_default(True)
        self.set_can_focus(True)
        
    def configure_handlers(self):
        self.set_events(0)

        self.add_events(gtk.gdk.EXPOSURE_MASK)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.add_events(gtk.gdk.BUTTON_MOTION_MASK)
        #self.add_events(gtk.gdk.KEY_PRESS_MASK)

        #self.expose_id = self.connect("expose-event", self.expose)
        self.connect("expose-event", self.expose)
        self.connect("button-press-event", self.press)
        self.connect("button-release-event", self.release)
        self.motion_id = self.connect("motion-notify-event", self.motion)
        #self.connect("key-press-event", self.key_press)

    def install_signals(self):
        gobject.signal_new("select", BaseCanvas, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        gobject.signal_new("edit-child", BaseCanvas, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
        
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
        
class Canvas(BaseCanvas): ### MIDDLE-LEVEL CODE HERE
    """This class represents a canvas"""

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
        #self.paper = None
        self.clipboard = None

    #def key_press(self, widget, event):
    #    pass

    #def update_cursor(self, widget, direction):
    #    if direction == NORTHWEST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER))
    #    elif direction == NORTH:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_SIDE))
    #    elif direction == NORTHEAST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_RIGHT_CORNER))
    #    elif direction == WEST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_SIDE))
    #    elif direction == EAST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.RIGHT_SIDE))
    #    elif direction == SOUTHWEST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_LEFT_CORNER))
    #    elif direction == SOUTH:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_SIDE))
    #    elif direction == SOUTHEAST:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER))
    #    elif direction == 8:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
    #    elif direction == 9:
    #        widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))

    def move(self, child, x, y):
        child.x = self.grid.nearest(x - child.offset.x)
        child.y = self.grid.nearest(y - child.offset.y)
        
    def resize(self, child, x, y):
        def set_position(child, x, y, width, height):
            #print x, y, width, height
            if (width >= 0) and (height >= 0):
                (child.x, child.y, child.width, child.height) = (x, y, width, height)
                
        if child.direction == EAST:
            _x = child.x
            _y = child.y
            _width = self.grid.nearest(child.offset.width + (x - child.offset.x))
            _height = child.height
            set_position(child, _x, _y, _width, _height)
        elif child.direction == NORTH:
            _x = child.x
            _y = self.grid.nearest(y - child.handler.control[NORTH].offset.y)
            _width = child.width
            _height = self.grid.nearest(child.offset.height + (child.offset.y - y))
            set_position(child, _x, _y, _width, _height)
        elif child.direction == SOUTH:
            _x = child.x
            _y = child.y
            _width = child.width
            _height = self.grid.nearest(child.offset.height + (y - child.offset.y))
            set_position(child, _x, _y, _width, _height)
        elif child.direction == WEST:
            _x = self.grid.nearest(x - child.handler.control[WEST].offset.x)
            _y = child.y
            _width = self.grid.nearest(child.offset.width + (child.offset.x - x))
            _height = child.height
            set_position(child, _x, _y, _width, _height)
        elif child.direction == SOUTHEAST:
            _x = child.x
            _y = child.y
            _width = self.grid.nearest(child.offset.width + (x - child.offset.x))
            _height = self.grid.nearest(child.offset.height + (y - child.offset.y))
            set_position(child, _x, _y, _width, _height)
        elif child.direction == SOUTHWEST:
            _x = self.grid.nearest(x - child.handler.control[SOUTHWEST].offset.x)
            _y = child.y
            _width = self.grid.nearest(child.offset.width + (child.offset.x - x))
            _height = self.grid.nearest(child.offset.height + (y - child.offset.y))
            set_position(child, _x, _y, _width, _height)
        elif child.direction == NORTHEAST:
            _x = child.x
            _y = self.grid.nearest(y - child.handler.control[NORTHEAST].offset.y)
            _width = self.grid.nearest(child.offset.width + (x - child.offset.x))
            _height = self.grid.nearest(child.offset.height + (child.offset.y - y))
            set_position(child, _x, _y, _width, _height)
        elif child.direction == NORTHWEST:
            _x = self.grid.nearest(x - child.handler.control[NORTHWEST].offset.x)
            _y = self.grid.nearest(y - child.handler.control[NORTHWEST].offset.y)
            _width = self.grid.nearest(child.offset.width + (child.offset.x - x))
            _height = self.grid.nearest(child.offset.height + (child.offset.y - y))
            set_position(child, _x, _y, _width, _height)
        else:
            return False
      
        return True
      
    def release(self, widget, event):
        """
        This code is executed when you release the mouse button
        """
        if self.selection.active:
            self.unselect_all()
            for child in sorted(self.children, key=lambda child: child.z):
                if child.in_selection(self.selection):
                    child.selected = True
                    self.emit("select", child)
                elif child.resize:
                    child.resize ^= 1
            self.selection.active = False

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
        self.horizontal_ruler.motion(self.horizontal_ruler, event, True)
        self.vertical_ruler.motion(self.vertical_ruler, event, True)
        self.disconnect(self.motion_id)
        x = event.x / self.zoom - self.origin.x
        y = event.y / self.zoom - self.origin.y

        def get_direction_for_child_at_position(x, y, origin, children):
            for child in children:
                if child.selected and child.at_position(x, y) and child.handler.at_position(x + origin.x, y + origin.y):
                        direction = child.handler.get_direction(x + origin.x, y + origin.y)
                        widget.bin_window.set_cursor(child.get_cursor(direction))
                        return direction
            return NONE

        direction = get_direction_for_child_at_position(x, y, self.origin, self.children)

        if not self.stop_cursor_change:
            if direction == NONE:
                if event.state & gtk.gdk.BUTTON1_MASK:
                    widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
                elif self.pick:
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
                    if child.resize:
                        self.emit("edit-child", child)
                        if not self.resize(child, x, y):
                            x = self.grid.nearest(x)
                            y = self.grid.nearest(y)
                            child.transform(child.direction, x, y)
                    else:
                        self.move(child, x, y)
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
            child.resize = True
            child.x = self.grid.nearest(event.x)
            child.y = self.grid.nearest(event.y)
            child.width = 0
            child.height = 0
            self.add(child)

            child.offset.x = event.x
            child.offset.y = event.y
            child.offset.width = child.width
            child.offset.height = child.height

            child.direction = SOUTHEAST
            child.handler.control[child.direction].offset.x = event.x - child.x
            child.handler.control[child.direction].offset.y = event.y - child.y
            widget.bin_window.set_cursor(gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER))
            self.stop_cursor_change = True
            return True

        selected = False
        move = False
        resize = False
        self.unselect_all()
        for child in sorted(self.children, key=lambda child: child.z, reverse=True):
            if child.at_position(event.x, event.y):
                if child.selected:
                    move = True
                selected = True
                child.selected = True
                if child.handler.at_position(event.x + self.origin.x, event.y + self.origin.y):
                    child.offset.x = event.x
                    child.offset.y = event.y
                    child.offset.width = child.width
                    child.offset.height = child.height
                    child.resize = True
                    child.direction = child.handler.get_direction(event.x + self.origin.x, event.y + self.origin.y)
                    child.handler.control[child.direction].offset.x = event.x - child.x
                    child.handler.control[child.direction].offset.y = event.y - child.y
                    resize = True
                    self.stop_cursor_change = True
                break

        if not resize:
            for child in self.children:
                child.resize = False
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
        context = widget.bin_window.cairo_create()
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
        return True

    add = lambda self, child: self.children.append(child)

    #update = lambda self: self.queue_draw()
    def update(self):
        if not self.updated:
            pass
        self.queue_draw()

class ExtendedCanvas(Canvas): ### HIGH-LEVEL CODE HERE
    """This class represents a canvas"""

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
        self.unselect_all()
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
        self.queue_draw()

    def select_all(self, *args):
        for child in self.children:
            child.selected = True
        self.queue_draw()

    def unselect_all(self, *args):
        for child in self.children:
            child.selected = False
        self.queue_draw()

    def select_last(self, *args):
        self.children[len(self.children) - 1].selected = True
        self.queue_draw()

    def bring_to_back(self, *args):
        for child in self.children:
            if child.selected:
                child.z -= 1
            else:
                child.z += 1
        self.queue_draw()

    def bring_to_front(self, *args):
        for child in self.children:
            if child.selected:
                child.z += 1
            else:
                child.z -= 1
        self.queue_draw()

    def paper_center_horizontal(self, *args):
        for child in self.children:
            if child.selected:
                child.x = int((self.pages[0].width - child.width) / 2 - self.border)
        self.queue_draw()

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
        self.queue_draw()

    def toggle_guides(self, *args):
        self.guides.active ^= 1
        self.queue_draw()

    def toggle_margins(self, *args):
        for page in self.pages:
            page.active ^= 1
        self.queue_draw()

    def get_filename(self, filename, extension):
        if not filename.endswith("." + extension):
            return filename + "." + extension
        else:
            return filename

    def save_to_pdf(self, filename):
        # TODO: fix save to PDF
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
                value = attributes["value"]
                internal = attributes["internal"]
                if internal == "true":
                    #code = "object.%s = %s" % (attribute, value)
                    #eval(code, dict({"object": object}))
                    # XXX XXX
                    #print value
                    value = int(round(float(value))) # XXX XXX
                    if attribute == 'x':
                        object.x = value
                    elif attribute == 'y':
                        object.y = value
                    elif attribute == 'z':
                        object.z = value
                    elif attribute == 'width':
                        object.width = value
                    elif attribute == 'height':
                        object.height = value
                        # XXX XXX
                else:
                    #if not object.__name__ == 'BarCode': # XXX
                    if not attribute == 'type' and not attribute == 'code': # XXX
                        #print attribute, value
                        object.set_property(attribute, value)
                        print "setting ", attribute, " to ", value
                    else:
                        pass # FIXME
                        #print attribute, value

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

        self.queue_draw()

    def serialize(self):
        text = "<document page=\"1\">\n"
        for child in self.children:
            text += child.serialize()
        text += "</document>\n"
        return text
        
class TestingCanvas(ExtendedCanvas): ### TESTING CODE HERE
    """This class represents a canvas"""

    def __init__(self):
        ExtendedCanvas.__init__(self)

        print _("WARNING: You are using a testing canvas.")

    def add_box_separator_vertical(self, *args):
        for child in self.children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_vertical(child.width / 2)
        self.queue_draw()

    def add_box_separator_horizontal(self, *args):
        for child in self.children:
            if child.selected and child.__name__ == 'Box':
                child.add_separator_horizontal(child.height / 2)
        self.queue_draw()
