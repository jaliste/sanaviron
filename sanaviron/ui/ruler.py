#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
import gtk

if platform.system() != 'Windows':
    gtk.threads_init()

import cairo
import pango
import pangocairo

class HorizontalRuler(gtk.Viewport):
    """This class represents a horizontal ruler"""

    def __init__(self):
        gtk.Viewport.__init__(self)
        self.set_size_request(-1, 25)

        self.x = 0
        self.tags = list()
        self.zoom = 1.0
        self.layout = gtk.Layout()
        self.add(self.layout)

        self.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.layout.add_events(gtk.gdk.EXPOSURE_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)

        self.connect("motion-notify-event", self.motion)
        self.connect("button-release-event", self.release)
        self.layout.connect("expose-event", self.expose)

    def motion(self, widget, event):
        self.x = event.x
        self.queue_draw()
        return True

    def release(self, widget, event):
        self.tags.append(event.x)
        self.queue_draw()
        return True

    def expose(self, widget, event):
        def paint_lines(context, x, left, width, size, zoom):
            while x <= width:
                context.move_to(x * zoom, left)
                context.line_to(x * zoom, width)
                x += size

        context = widget.bin_window.cairo_create()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        width, height = self.window.get_size()

        dash = list()
        context.set_dash(dash)
        context.set_line_width(1)
        paint_lines(context, 25, 18, width, 10, self.zoom)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        context.set_line_width(1.0)
        paint_lines(context, 25, 10, width, 50, self.zoom)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        context.set_line_width(2)
        paint_lines(context, 25, 8, width, 100, self.zoom)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        border = 5
        context.set_line_width(3)
        for x in self.tags:
            context.move_to(x, border)
            context.line_to(x, height - border)
        context.set_source_rgb(0.75, 0.0, 0.0)
        context.stroke()

        if (self.x):
            border = 2
            context.set_line_width(1)
            context.move_to(self.x, border)
            context.line_to(self.x, height)
            context.set_source_rgba(0.0, 0.0, 0.75)
            context.stroke()

        context = pangocairo.CairoContext(context) # XXX
        layout = pangocairo.CairoContext.create_layout(context)
        if platform.system() == 'Windows': # to avoid console warning on windows
            fontname = 'Sans'
        else:
            fontname = 'Ubuntu'
        size = 8
        description = '%s %d' % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        text = str(int(self.x))
        layout.set_markup(text)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.move_to(self.x + 2, 0)
        context.show_layout(layout)
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        return True


class VerticalRuler(gtk.Viewport):
    """This class represents a vertical rule"""

    def __init__(self):
        gtk.Viewport.__init__(self)
        self.set_size_request(25, -1)

        self.y = 0
        self.tags = list()

        self.layout = gtk.Layout()
        self.add(self.layout)

        self.layout.add_events(gtk.gdk.EXPOSURE_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.POINTER_MOTION_MASK)

        self.layout.connect("expose-event", self.expose)
        self.connect("button-release-event", self.release)
        self.connect("motion-notify-event", self.motion)

    def motion(self, widget, event):
        self.y = event.y
        self.queue_draw()
        return True

    def release(self, widget, event):
        self.tags.append(event.y)
        self.queue_draw()
        return True

    def expose(self, widget, event):
        def paint_lines(context, y, left, width, size):
            while y <= height:
                context.move_to(left, y)
                context.line_to(width, y)
                y += size

        context = widget.bin_window.cairo_create()
        context.set_antialias(cairo.ANTIALIAS_NONE)
        width, height = self.window.get_size()

        dash = list()
        context.set_dash(dash)

        context.set_line_width(1.0)
        y = 0
        left = 18
        size = 10
        paint_lines(context, y, left, width, size)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        context.set_line_width(1.0)
        y = 0
        left = 10
        size = 50
        paint_lines(context, y, left, width, size)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        context.set_line_width(2)
        y = 0
        left = 8
        size = 100
        paint_lines(context, y, left, width, size)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()

        border = 4
        context.set_line_width(3)
        for y in self.tags:
            context.move_to(border, y)
            context.line_to(width - border, y)
        context.set_source_rgb(0.75, 0.0, 0.0)
        context.stroke()

        if (self.y):
            border = 2
            context.set_line_width(1)
            context.move_to(border, self.y)
            context.line_to(width - border, self.y)
            context.set_source_rgb(0.0, 0.0, 0.75)
            context.stroke()

        # text
        pangocontext = pangocairo.CairoContext(context) # XXX
        layout = pangocairo.CairoContext.create_layout(pangocontext)
        if platform.system() == 'Windows': # to avoid console warning on windows
            fontname = 'Sans'
        else:
            fontname = 'Ubuntu'
        size = 8
        description = '%s %d' % (fontname, size)
        font = pango.FontDescription(description)
        layout.set_justify(True)
        layout.set_font_description(font)
        text = str(int(self.y))
        layout.set_markup(text)
        context.set_source_rgb(0.0, 0.0, 0.0)
        context.move_to(2, self.y)
        context.show_layout(layout)
        context.set_antialias(cairo.ANTIALIAS_DEFAULT)
        return True

if __name__ == '__main__':
    horizontal_window = gtk.Window()
    horizontal_window.connect("delete-event", gtk.main_quit)
    horizontal_ruler = HorizontalRuler()
    horizontal_window.add(horizontal_ruler)
    horizontal_window.show_all()
    vertical_window = gtk.Window()
    vertical_window.connect("delete-event", gtk.main_quit)
    vertical_ruler = VerticalRuler()
    vertical_window.add(vertical_ruler)
    vertical_window.show_all()
    gtk.main()
