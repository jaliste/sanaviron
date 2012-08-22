#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

from objects.gradient import Gradient
from objects.gradientcolor import GradientColor
from objects import LINEAR

grad = Gradient(type=LINEAR, name="", x=0, y=0, x1=0, y1=0)
for index in range(11):
    grad.add_new_color(GradientColor(index * 0.1, index * 0.1, index * 0.1, 1.0, index * 0.1))
    grad.update()

class GradientLine(gtk.Viewport):
    def __init__(self, canvas=None):
        gtk.Viewport.__init__(self)
        self.set_size_request(-1, 70)
        self.set_shadow_type(gtk.SHADOW_NONE)
        #self.canvas = canvas
        self.width = 0
        self.height = 0
        self._motion = False
        self.selected = -1
        self.x = 0
        self.move = False
        self.g = grad

        self.layout = gtk.Layout()
        self.add(self.layout)

        self.layout.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.layout.connect("button-press-event", self.press)
        self.layout.add_events(gtk.gdk.EXPOSURE_MASK)
        self.layout.connect("expose-event", self.expose)
        self.layout.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.layout.connect("button-release-event", self.release)
        self.layout.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.layout.connect("motion-notify-event", self.motion)
        self.layout.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)
        self.layout.connect("leave-notify-event", self.leave)
        self.layout.add_events(gtk.gdk.WINDOW_STATE)
        self.layout.connect("window_state_event", self.update_resize)

    def update_resize(self, widget, event):
        self.g.change_size(0, 0, self.width, 0)
        self.g.update()
        self.queue_draw()
        return True

    def update(self):
        self.queue_draw()

    def motion(self, widget, event):
        self._motion = True
        self.x = event.x
        if self.move:
            if self.selected >= 0:
                self.g.set_position(self.selected, event.x / self.width)
                self.g.update()
        self.queue_draw()
        return True

    def leave(self, widget, event):
        self._motion = False
        self.x = event.x
        self.queue_draw()
        return True

    def press(self, widget, event):
        self.move = True
        cnt = len(self.g.colors)
        if cnt > 0:
            for col in range(0, cnt):
                if (self.g.colors[col].position > (event.x / self.width - 0.01)) and (
                    self.g.colors[col].position < (event.x / self.width + 0.01)):
                    self.selected = col
                    break
                else:
                    self.selected = -1
        else:
            self.g.add_new_color(GradientColor(1, 0.1, 0.1, 1.0, event.x / self.width))
            self.g.update()

        if self.selected == -1:
            col = GradientColor(1, 1, 0.1, 1.0, event.x / self.width)
            self.g.add_new_color(col)
            self.g.update()

        self.queue_draw()
        return True

    def release(self, widget, event):
        self.move = False
        self.queue_draw()
        return True

    def expose(self, widget, event):
        context = widget.bin_window.cairo_create()
        self.width, self.height = self.window.get_size()
        self.g.change_size(0, 0, self.width, 0)
        context.rectangle(0, 0, self.width, self.height)
        context.set_source(self.g.gradient)
        context.fill_preserve()

        if self._motion and not self.move:
            context.new_path()
            dash = list()
            context.set_dash(dash)
            context.set_line_width(2)
            context.move_to(self.x, 0)
            context.line_to(self.x, 30)
            context.move_to(self.x, self.height - 30)
            context.line_to(self.x, self.height)

            if 1: # experimental code: find opossite color in case of position of pattern has same color os cursor
                scol = sorted(self.g.colors,
                    key=lambda color: color.position) # better in __init__ and update when necessary
                cnt = len(scol)
                rx = self.x / self.width
                index = 0
                for col in scol:
                    if rx < col.position:
                        for c in range(0, cnt):
                            if self.g.colors[c].position == col.position:
                                index = c
                                break
                        break
                        # what is the oposite algorithm?
                        # my personal approach:
                    # white is 1,1,1
                # black is 0,0,0
                # neutral gray is .5,.5,.5
                # the oposite of white is black, then 1,1,1===0,0,0 => 1-1,1-1,1-1===0,0,0
                # the oposite of black is white, then 0,0,0===1,1,1 => 1-0,1-0,1-0===1,1,1
                # the oposite of neutral gray is ???, then .5,.5,.5===?,?,? => 1-.5,1-.5,1-.5===.5,.5,.5 (error, use default)
                # define limits: 2.5>x>7.5

                r = self.g.colors[index].red
                g = self.g.colors[index].green
                b = self.g.colors[index].blue
                l = 1 - (r + g + b) / 3.0
                if l >= 0.5:
                    l = 1
                else:
                    l = 0
                r, g, b = l, l, l

                """if 2.5 >= self.g.colors[index].red and self.g.colors[index].red >= 7.5:
                r = 1-self.g.colors[index].red
              else:
                r = 0.3
              if 2.5 >= self.g.colors[index].green and self.g.colors[index].green >= 7.5:
                g = 1-self.g.colors[index].green
              else:
                g = 0.3
              if 2.5 >= self.g.colors[index].blue and self.g.colors[index].blue >= 7.5:
                b = 1-self.g.colors[index].blue
              else:
                b = 0.3
              a = self.g.colors[index].alpha"""

                context.set_source_rgba(r, g, b, 1.0)
            else:
                context.set_source_rgba(0.3, 0.2, 0.2, 1.0) # Denis default color

            context.stroke()

        for color in range(len(self.g.colors)):
            if color == self.selected:
                delta = 10
            else:
                delta = 0

            context.new_path()
            pos = self.width * self.g.colors[color].position
            context.move_to(pos - 5, 0)
            context.line_to(pos + 5, 0)
            context.line_to(pos, 20)
            context.line_to(pos - 5, 0)
            context.set_source_rgb(self.g.colors[color].alpha, self.g.colors[color].alpha, self.g.colors[color].alpha)
            context.fill_preserve()
            if delta:
                context.move_to(pos, 20)
                context.line_to(pos, 20 + delta)
            context.set_source_rgba(0.44, 0.62, 0.81, 1.0)
            context.stroke()

            context.new_path()
            if delta:
                context.move_to(pos, self.height - 20 - delta)
                context.line_to(pos, self.height - 20)
            context.move_to(pos, self.height - 20)
            context.line_to(pos + 5, self.height)
            context.line_to(pos - 5, self.height)
            context.line_to(pos, self.height - 20)
            context.set_source_rgb(self.g.colors[color].red, self.g.colors[color].green, self.g.colors[color].blue)
            context.fill_preserve()
            context.set_source_rgba(0.44, 0.62, 0.81, 0.7)
            context.stroke()

        return False


class GradientEditor(gtk.VBox):
    def __init__(self, canvas=None):
        gtk.VBox.__init__(self)

        table = gtk.Table(5, 4, False)
        self.pack_start(table)
        self.combobox = gtk.combo_box_new_text()
        table.attach(self.combobox, 1, 2, 0, 1, gtk.FILL | gtk.EXPAND, 0)

        self.gl = GradientLine(canvas)
        table.attach(self.gl, 1, 2, 1, 4, gtk.FILL | gtk.EXPAND, 0)

        new_color = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        new_color.add(image)
        table.attach(new_color, 2, 3, 0, 1, 0, 0, 10)

        button = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
        button.add(image)
        button.connect("clicked", self.forward)
        table.attach(button, 2, 3, 2, 3, 0, 0, 10)

        button = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
        button.add(image)
        button.connect("clicked", self.back)
        table.attach(button, 0, 1, 2, 3, 0, 0, 10)

        self.show_all()

    def forward(self, widget):
        if self.gl.selected < len(self.gl.g.colors) - 1:
            self.gl.selected += 1
        else:
            self.gl.selected = -1
        self.gl.update()

    def back(self, widget):
        if self.gl.selected > -1:
            self.gl.selected -= 1
        else:
            self.gl.selected = len(self.gl.g.colors) - 1
        self.gl.update()

if __name__ == '__main__':
    horizontal_window = gtk.Window()
    horizontal_window.set_default_size(500, 100)
    horizontal_window.connect("delete-event", gtk.main_quit)

    ge = GradientEditor()
    horizontal_window.add(ge)

    horizontal_window.show_all()
    gtk.main()
