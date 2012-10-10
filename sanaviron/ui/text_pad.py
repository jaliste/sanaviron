#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
from objects.signalized import Signalized

class TextPad(gtk.VBox, Signalized):
    """This class represents a minimal text editor"""

    def __init__(self):
        gtk.VBox.__init__(self)

        self.position = 0

        handle = gtk.HandleBox()
        handle.set_handle_position(gtk.POS_LEFT)
        self.pack_start(handle, False, False)

        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        #toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)
        toolbar.set_icon_size(gtk.ICON_SIZE_MENU)
        handle.add(toolbar)

        position = 0
        button = gtk.ToolButton(gtk.STOCK_BOLD)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_ITALIC)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_UNDERLINE)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_STRIKETHROUGH)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_JUSTIFY_LEFT)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_JUSTIFY_RIGHT)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_JUSTIFY_CENTER)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_JUSTIFY_FILL)
        toolbar.insert(button, position)

        position += 1
        separator = gtk.SeparatorToolItem()
        toolbar.insert(separator, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_INDENT)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_UNINDENT)
        toolbar.insert(button, position)

        area = gtk.ScrolledWindow()
        area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        adjustment = area.get_vadjustment()
        adjustment.need_scroll = True
        adjustment.connect("changed", self.update_adjustment)
        adjustment.connect("value-changed", self.update_value)
        entry = gtk.TextView()
        entry.connect("move-cursor", self.move)
        entry.set_size_request(-1, 100)
        self.buffer = entry.get_buffer()
        #self.disconnect_handler = buffer.connect("changed", self.changed)
        self.buffer.connect("insert-text", self.update_scroll, entry)
        self.buffer.connect("changed", self.changed)
        #area.add_with_viewport(entry)
        area.add(entry)
        #entry.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        entry.set_wrap_mode(gtk.WRAP_CHAR)
        self.add(area)

        self.install_signal("cursor-moved")

    def get_cursor_position(self):
        mark = self.buffer.get_insert()
        iter = self.buffer.get_iter_at_mark(mark)
        return iter.get_offset()

    def move(self, view, step, count, extend):
        self.position = self.get_cursor_position()
        self.emit("cursor-moved", self.position)

    def changed(self, buffer):
        self.position = self.get_cursor_position()
        self.emit("cursor-moved", self.position)

    def update_scroll(self, buffer, iter, text, length, view):
        mark = buffer.create_mark("end", iter, False)
        view.scroll_mark_onscreen(mark)

    def update_adjustment(self, adjustment):
        if adjustment.need_scroll:
            adjustment.set_value(adjustment.upper - adjustment.page_size)
            adjustment.need_scroll = True

    def update_value(self, adjustment):
        adjustment.need_scroll = abs(
            adjustment.value + adjustment.page_size - adjustment.upper) < adjustment.step_increment

    def set_text(self, text):
        self.buffer.set_text(text)

if __name__ == '__main__':
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    text_pad = TextPad()
    window.add(text_pad)
    window.show_all()
    gtk.main()
