#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
import gtksourceview

class SourcePad(gtk.VBox):
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

        area = gtk.ScrolledWindow()
        area.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        adjustment = area.get_vadjustment()
        adjustment.need_scroll = True
        adjustment.connect("changed", self.update_adjustment)
        adjustment.connect("value-changed", self.update_value)
        source_buffer = gtksourceview.SourceBuffer()
        entry = gtksourceview.SourceView(source_buffer)
        entry.set_size_request(-1, 100)
        self.buffer = entry.get_buffer()
        #self.disconnect_handler = buffer.connect("changed", self.changed)
        self.buffer.connect("insert-text", self.update_scroll, entry)
        #area.add_with_viewport(entry)
        area.add(entry)
        #entry.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        entry.set_wrap_mode(gtk.WRAP_CHAR)
        self.add(area)

        entry.set_show_line_numbers(True)
        entry.set_show_line_markers(True)
        entry.set_tabs_width(8)
        entry.set_auto_indent(True)
        entry.set_insert_spaces_instead_of_tabs(False)
        entry.set_show_margin(True)
        entry.set_margin(30)
        #entry.set_marker_pixbuf(marker_type, pixbuf)
        entry.set_smart_home_end(True)

        manager = gtksourceview.SourceLanguagesManager()

        #for language in manager.get_available_languages():
        #  name = language.get_name()
        #  mime = language.get_mime_types()
        #  print "%s\t\t%s\n" % (name, mime)

        #language = manager.get_language_from_mime_type("text/x-python")
        language = manager.get_language_from_mime_type("text/x-sql")

        source_buffer.set_check_brackets(True)
        #source_buffer.set_bracket_match_style(style)
        source_buffer.set_highlight(True)
        source_buffer.set_max_undo_levels(10)
        source_buffer.set_language(language)
        #source_buffer.set_escape_char("\e")

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

if __name__ == '__main__':
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    source_pad = SourcePad()
    window.add(source_pad)
    window.show_all()
    gtk.main()
