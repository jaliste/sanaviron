#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
import gtksourceview2 as gtksourceview

class SourcePad(gtk.ScrolledWindow):
    """This class represents a source code editor""" # No used yet!

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        adjustment = self.get_vadjustment()
        adjustment.need_scroll = True
        adjustment.connect("changed", self.update_adjustment)
        adjustment.connect("value-changed", self.update_value)
        self.buffer = gtksourceview.Buffer()
        entry = gtksourceview.View(self.buffer)
        entry.set_size_request(-1, 100)
        #self.disconnect_handler = buffer.connect("changed", self.changed)
        self.buffer.connect("insert-text", self.update_scroll, entry)
        #self.add_with_viewport(entry)
        self.add(entry)
        entry.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        entry.set_wrap_mode(gtk.WRAP_CHAR)

        entry.set_show_line_numbers(True)
        entry.set_show_line_marks(True)
        entry.set_tab_width(8)
        entry.set_auto_indent(True)
        entry.set_insert_spaces_instead_of_tabs(False)
        entry.set_show_right_margin(True)
        entry.set_right_margin(30)
        #entry.set_marker_pixbuf(marker_type, pixbuf)
        entry.set_smart_home_end(True)

        self.buffer.set_highlight_syntax(True)
        self.buffer.set_max_undo_levels(10)
        self.buffer.set_highlight_matching_brackets(True)
        self.set_language("python") # default

    def set_language(self, language):
        manager = gtksourceview.LanguageManager()
        srclang = manager.get_language(language)
        self.buffer.set_language(srclang)

    def update_scroll(self, buffer, iter, text, length, view):
        mark = buffer.create_mark("end", iter, False)
        view.scroll_mark_onscreen(mark)

    # Methods for update the scrollbars of text area.
    def update_adjustment(self, adjustment):
        if adjustment.need_scroll:
            adjustment.set_value(adjustment.upper - adjustment.page_size)
            adjustment.need_scroll = True

    def update_value(self, adjustment):
        adjustment.need_scroll = abs(
            adjustment.value + adjustment.page_size - adjustment.upper) < adjustment.step_increment

class CodeEditor(gtk.VBox):
    """This class represents a source code editor""" # No used yet!

    def __init__(self):
        gtk.VBox.__init__(self)

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
        button = gtk.ToolButton(gtk.STOCK_MEDIA_PLAY)
        toolbar.insert(button, position)

        position += 1
        button = gtk.ToolButton(gtk.STOCK_MEDIA_STOP)
        toolbar.insert(button, position)

        self.editor = SourcePad()
        self.add(self.editor)

if __name__ == '__main__':
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    editor = CodeEditor()
    window.add(editor)
    window.show_all()
    gtk.main()
