#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

from ui.button import Button
from ui.entry import LinearEntry, AngularEntry
from objects import *
from objects.barcode import barcodes
from objects.charts import *
from objects.color import Color
from ui.text_pad import TextPad
from ui.columns_editor import ColumnsEditor
from ui.gradienteditor import GradientEditor
import sys

class Form(gtk.VBox):
    """This class represents a properties form"""

    def __init__(self, canvas):
        gtk.VBox.__init__(self)
        self._canvas = canvas
        #self.set_border_width(1)
        #self.set_spacing(1)

        self.table = None
        self.entries = 0

    def add_section(self, caption):
        expander = gtk.Expander('<b>' + caption + '</b>')
        expander.set_expanded(True)
        label = expander.get_label_widget()
        label.set_use_markup(True)
        self.add(expander)

        table = gtk.Table()
        table.set_row_spacings(6)
        table.set_col_spacings(12)
        alignment = gtk.Alignment(0.0, 0.0, 1.0, 0.0)
        alignment.add(table)
        alignment.set_padding(6, 0, 12, 0)
        expander.add(alignment)

        self.table = table
        self.entries = 0

    def add_entry(self, group, caption, entry, expanded=False):
        if caption:
            label = gtk.Label(caption + ':')
            group.add_widget(label)
            label.set_alignment(0.0, 0.5)
            self.table.attach(label, 0, 1, self.entries, self.entries + 1, gtk.FILL, 0)
            alignment = gtk.Alignment(0.0, 0.5, float(expanded))
            alignment.add(entry)
            self.table.attach(alignment, 1, 2, self.entries, self.entries + 1, gtk.EXPAND | gtk.FILL, 0)
        else:
            self.table.attach(entry, 0, 2, self.entries, self.entries + 1, gtk.EXPAND | gtk.FILL, 0)
        self.entries += 1


class Observer:
    def __init__(self):
        self.observables = dict()

    def install_observable(self, name, widget):
        self.observables[name] = widget

    def get_observable(self, name):
        return self.observables[name]


class PositionedObjectForm(Form):
    """TODO"""

    def __init__(self, group, canvas):
        Form.__init__(self, canvas)

        self.add_section(_("Position"))

        entry = LinearEntry()
        self.add_entry(group, _("Horizontal"), entry)

        entry = LinearEntry()
        self.add_entry(group, _("Vertical"), entry)


class AngledObjectForm(Form):
    """TODO"""

    def __init__(self, group):
        Form.__init__(self)

        self.add_section(_("Angle"))

        entry = AngularEntry()
        self.add_entry(group, _("Start Angle"), entry)

        entry = AngularEntry()
        self.add_entry(group, _("Stop Angle"), entry)


class SizedObjectForm(PositionedObjectForm):
    """TODO"""

    def __init__(self, group, canvas):
        PositionedObjectForm.__init__(self, group, canvas)

        self.add_section(_("Size"))

        entry = LinearEntry()
        self.add_entry(group, _("Width"), entry)

        entry = LinearEntry()
        self.add_entry(group, _("Height"), entry)


class ColorizedObjectForm(SizedObjectForm):
    """TODO"""

    def __init__(self, group, canvas):
        PositionedObjectForm.__init__(self, group, canvas)

        self.add_section(_("Color"))

        entry = gtk.ColorButton()
        entry.set_use_alpha(True)
        entry.connect("color-set", self.set_stroke_color)
        self.add_entry(group, _("Stroke"), entry)

        entry = gtk.ColorButton()
        entry.set_use_alpha(True)
        entry.connect("color-set", self.set_fill_color)
        self.add_entry(group, _("Fill"), entry)

        if "--debug" in sys.argv:
            entry = gtk.Label(" ")
            self.add_entry(group, _("Gradient"), entry)
            entry = GradientEditor(self._canvas)
            self.add(entry)

    def set_stroke_color(self, widget):
        for child in self._canvas.children:
            if child.selected:
                color = Color(r=widget.get_color().red_float, g=widget.get_color().green_float,
                    b=widget.get_color().blue_float, a=widget.get_alpha() / 65535.0)
                child.set_stroke_color(color)
                self._canvas.queue_draw()

    def set_fill_color(self, widget):
        for child in self._canvas.children:
            if child.selected:
                color = Color(r=widget.get_color().red_float, g=widget.get_color().green_float,
                    b=widget.get_color().blue_float, a=widget.get_alpha() / 65535.0)
                child.set_fill_color(color)
                self._canvas.queue_draw()


class Properties(gtk.ScrolledWindow):
    """Esta clase representa la paleta de propiedades"""

    def __init__(self, canvas):
        gtk.ScrolledWindow.__init__(self)

        self.observer = Observer()

        self.objects = dict()

        self.canvas = canvas # FIXME

        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        properties = gtk.VBox()
        self.add_with_viewport(properties)

        group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

        #---START-------------------------------------------------------
        button = Button(_("General properties"))
        properties.pack_start(button, False, False)

        form = Form(canvas)
        button.add(form)

        form.add_section(_("Units"))

        entry = gtk.combo_box_new_text()
        entry.append_text(CENTIMETERS)
        entry.append_text(MILLIMETERS)
        entry.append_text(DOTS)
        entry.append_text(INCHES)
        entry.set_active(1)

        form.add_entry(group, _("Preferred linear unit"), entry)

        entry = gtk.combo_box_new_text()
        entry.append_text(DEGREES)
        entry.append_text(RADIANS)
        entry.set_active(1)

        form.add_entry(group, _("Preferred angular unit"), entry)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Document properties"))
        properties.pack_start(button, False, False)

        form = Form(canvas)
        button.add(form)

        form.add_section(_("Size"))

        entry = LinearEntry()
        form.add_entry(group, _("Width"), entry)

        entry = LinearEntry()
        form.add_entry(group, _("Height"), entry)

        form.add_section(_("Margins"))

        entry = LinearEntry()
        form.add_entry(group, _("Top"), entry)

        entry = LinearEntry()
        form.add_entry(group, _("Bottom"), entry)

        entry = LinearEntry()
        form.add_entry(group, _("Left"), entry)

        entry = LinearEntry()
        form.add_entry(group, _("Right"), entry)

        form.add_section(_("Config"))

        entry = LinearEntry()
        form.add_entry(group, _("Grid size"), entry)

        entry = LinearEntry()
        form.add_entry(group, _("Guides size"), entry)

        entry = gtk.CheckButton(_("Show margins"))
        form.add_entry(group, None, entry)

        entry = gtk.CheckButton(_("Show guides"))
        form.add_entry(group, None, entry)

        entry = gtk.CheckButton(_("Show grid"))
        form.add_entry(group, None, entry)

        entry = gtk.CheckButton(_("Enable snap"))
        form.add_entry(group, None, entry)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Text properties"))
        self.objects["Text"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Format"))

        entry = gtk.FontButton()
        entry.connect("font-set", self.change_font)
        form.add_entry(group, _("Font"), entry)

        entry = gtk.CheckButton(_("Preserve aspect"))
        entry.connect("toggled", self.preserve)
        form.add_entry(group, None, entry)

        form.add_section(_("Text"))

        self.entry = TextPad()
        self.disconnect_handler = self.entry.buffer.connect("changed", self.changed)
        form.add_entry(group, None, self.entry)
        #---END---------------------------------------------------------

        #---START--------ARC properties-----------------------------------------------
        button = Button(_("Arc properties"))
        self.objects["Arc"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Angle"))
        self.angle_start = AngularEntry()
        form.add_entry(group, _("Start Angle"), self.angle_start)
        self.angle_start.spin.connect("value-changed", self.change_angle_start)

        self.angle_stop = AngularEntry()
        form.add_entry(group, _("Stop Angle"), self.angle_stop)
        self.angle_stop.spin.connect("value-changed", self.change_angle_stop)

        form.add_section(_("Other"))
        self.closed_btn = gtk.CheckButton()
        form.add_entry(group, _("Closed Arc"), self.closed_btn)
        self.closed_btn.connect("toggled", self.close_arc)

        self.closed_at_centre_btn = gtk.CheckButton()
        form.add_entry(group, _("Closed Arc at Centre"), self.closed_at_centre_btn)
        self.closed_at_centre_btn.connect("toggled", self.close_at_centre_arc)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Table properties"))
        self.objects["Table"] = button
        properties.pack_start(button, False, False)

        form = PositionedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Spacing"))

        entry = gtk.SpinButton()
        entry.set_digits(0)
        entry.set_increments(1, 2)
        entry.set_range(0, 1024)
        entry.set_value(1)
        entry.set_numeric(True)
        entry.set_wrap(False)
        form.add_entry(group, _("Vertical"), entry)

        entry = gtk.SpinButton()
        entry.set_digits(0)
        entry.set_increments(1, 2)
        entry.set_range(0, 1024)
        entry.set_value(0)
        entry.set_numeric(True)
        entry.set_wrap(False)
        form.add_entry(group, _("Horizontal"), entry)

        form.add_section(_("Size"))

        entry = gtk.SpinButton()
        entry.connect("value-changed", self.set_table_columns)
        entry.set_digits(0)
        entry.set_increments(1, 2)
        entry.set_range(0, 1024)
        entry.set_value(1)
        entry.set_numeric(True)
        entry.set_wrap(False)
        form.add_entry(group, _("Columns"), entry)

        entry = gtk.SpinButton()
        entry.connect("value-changed", self.set_table_rows)
        entry.set_digits(0)
        entry.set_increments(1, 2)
        entry.set_range(0, 1024)
        entry.set_value(0)
        entry.set_numeric(True)
        entry.set_wrap(False)
        form.add_entry(group, _("Rows"), entry)

        form.add_section(_("Color"))

        entry = gtk.ColorButton()
        form.add_entry(group, _("Stroke"), entry)

        entry = gtk.ColorButton()
        form.add_entry(group, _("Fill"), entry)

        form.add_section(_("Format"))

        entry = gtk.FontButton()
        entry.connect("font-set", self.set_table_font)
        form.add_entry(group, _("Font"), entry)

        form.add_section(_("Columns"))

        entry = ColumnsEditor()
        entry.add_column()
        entry.connect("width-edited", self.set_table_column_width)
        entry.connect("title-edited", self.set_table_column_title)
        self.observer.install_observable("table-columns-editor", entry)
        form.add_entry(group, None, entry)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Barcode properties"))
        self.objects["BarCode"] = button
        properties.pack_start(button, False, False)

        form = ColorizedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Barcode"))

        entry = gtk.combo_box_new_text()
        entry.connect("changed", self.changed_barcode_type)
        for type in barcodes:
            entry.append_text(type)
        form.add_entry(group, _("Type"), entry)

        entry = gtk.Entry()
        entry.connect("changed", self.changed_barcode_code)
        form.add_entry(group, _("Code"), entry)
        #---END---------------------------------------------------------

        # s/label.set_markup("<b>\([^<]\+\)<\/b>")/form.add_section(_("\1"))/
        # s/label = gtk.Label("\([^:]\+\):")/form.add_entry(group, _("\1"), entry)/
        # s/gtk.Table/Form/
        # s/table/form/g

        #---START-------------------------------------------------------
        button = Button(_("Image properties"))
        self.objects["Image"] = button
        properties.pack_start(button, False, False)

        form = SizedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Image"))


        def update_preview(dialog, preview):
            filename = dialog.get_preview_filename()
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
                preview.set_from_pixbuf(pixbuf)
                have_preview = True
            except:
                have_preview = False
            dialog.set_preview_widget_active(have_preview)

        dialog = gtk.FileChooserDialog(title="Source image file",
            #parent = self,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT),
            backend=None)

        preview = gtk.Image()

        dialog.set_preview_widget(preview)
        dialog.connect("update-preview", update_preview, preview)

        #dialog.set_transient_for(self)
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("PNG files")
        filter.add_mime_type("image/png")
        filter.add_pattern("*.png")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("JPG files")
        filter.add_mime_type("image/jpg")
        filter.add_pattern("*.jpg")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        dialog.connect("file-activated", self.changed_image_file)

        entry = gtk.FileChooserButton(dialog)
        form.add_entry(group, _("Image file"), entry, True)
        #---END---------------------------------------------------------

        #---START-------------------------------------------------------
        button = Button(_("Chart properties"))
        self.objects["Chart"] = button
        properties.pack_start(button, False, False)

        form = SizedObjectForm(group, canvas)
        button.add(form)

        form.add_section(_("Chart"))

        entry = gtk.combo_box_new_text()
        entry.connect("changed", self.changed_chart_type)
        for type in chart_types:
            entry.append_text(type)
        form.add_entry(group, _("Type"), entry)
        #---END---------------------------------------------------------

    def select(self, name, child):
        for key, object in self.objects.items():
            if key == name:
                object.show()

                if name == "Text":
                    text = child.get_property("text")
                    self.entry.set_text(text)
                if name == "BarCode":
                    code = child.get_property("code")
                    #self.entry.set_text(code) # TODO
            else:
                object.hide()

    def set_table_column_title(self, widget, column, title):
        for child in self.canvas.children:
            if child.__name__ == "Table" and child.selected:
                titles = child.get_property('titles').split(':')
                titles[column] = title
                titles = ':'.join(titles)
                child.set_property('titles', titles)
                self.canvas.queue_draw()
                break

    def set_table_column_width(self, widget, column, width):
        for child in self.canvas.children:
            if child.__name__ == "Table" and child.selected:
                columns = child.get_property('columns').split(':')
                columns[column] = str(width)
                columns = ':'.join(columns)
                child.set_property('columns', columns)
                self.canvas.queue_draw()
                break

    def set_table_columns(self, widget):
        n_columns = widget.get_value_as_int()
        for child in self.canvas.children:
            if child.__name__ == "Table" and child.selected:
                entry = self.observer.get_observable("table-columns-editor")
                columns = child.get_property('columns').split(':')
                titles = child.get_property('titles').split(':')
                if n_columns < len(columns):  # Eliminar columna
                    del columns[n_columns]
                    del titles[n_columns]
                    entry.remove_column()
                elif n_columns > len(columns):  # Agregar columna
                    columns.append('0')
                    title = _("Column %d") % n_columns
                    titles.append(title)
                    entry.add_column()
                else: # XXX ::: No deberían ser iguales
                    entry.add_column()
                columns = ':'.join(columns)
                #print titles
                titles = ':'.join(titles)
                child.set_property('columns', columns)
                child.set_property('titles', titles)
                self.canvas.queue_draw()
                break

    def set_table_rows(self, widget):
        rows = widget.get_value_as_int()
        for child in self.canvas.children:
            if child.__name__ == "Table" and child.selected:
                child.set_property('rows', rows)
                self.canvas.queue_draw()
                break

    def set_text_foreground(self, widget):
        color = widget.get_color()
        print color.red
        print color.green
        print color.blue

    def changed(self, buffer):
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end)
        for child in self.canvas.children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('text', text)
                #self.canvas.queue_draw()
                #break
        self.canvas.queue_draw()

        #mark = buffer.create_mark("end", end, False)
        #view.scroll_mark_onscreen(mark)

    def set_table_font(self, widget):
        font = widget.get_font_name()
        for child in self.canvas.children:
            if child.__name__ == "Table" and child.selected:
                child.set_property('font', font)
                self.canvas.queue_draw()
                break

    def close_arc(self, widget):
        state = widget.get_active()
        for child in self.canvas.children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('closed', int(state))
                self.canvas.queue_draw()
        self.closed_at_centre_btn.set_sensitive(state)

    def close_at_centre_arc(self, widget):
        state = widget.get_active()
        for child in self.canvas.children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('closed_at_centre', int(state))
                self.canvas.queue_draw()

    def change_angle_start(self, widget):
        val = widget.get_value()
        for child in self.canvas.children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('angle_start', val)
                self.canvas.queue_draw()

    def change_angle_stop(self, widget):
        val = widget.get_value()
        for child in self.canvas.children:
            if child.__name__ == "Arc" and child.selected:
                child.set_property('angle_stop', val)
                self.canvas.queue_draw()

    def change_font(self, widget):
        font = widget.get_font_name()
        for child in self.canvas.children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('font', font)
                self.canvas.queue_draw()
                break

    def preserve(self, widget):
        preserve = widget.get_active()
        for child in self.canvas.children:
            if child.__name__ == "Text" and child.selected:
                child.set_property('preserve', preserve)
                self.canvas.queue_draw()
                break

    def changed_barcode_type(self, widget):
        #selected = widget.get_active_text()
        #type = get_barcode_type_from_string(selected)
        type = widget.get_active()
        for child in self.canvas.children:
            if child.__name__ == "BarCode" and child.selected:
                child.set_property('type', type)
                self.canvas.queue_draw()
                break

    def changed_barcode_code(self, editable):
        code = editable.get_chars(0, -1)
        for child in self.canvas.children:
            if child.__name__ == "BarCode" and child.selected:
                child.set_property('code', code)
                self.canvas.queue_draw()
                break

    def changed_image_file(self, widget):
        filename = widget.get_filename()
        print filename
        if filename is not None:
            for child in self.canvas.children:
                if child.__name__ == "Image" and child.selected:
                    child.set_property('image', filename)
                    self.canvas.queue_draw()
                    break

    def changed_chart_type(self, widget):
        #selected = widget.get_active_text()
        #type = get_barcode_type_from_string(selected)
        type = widget.get_active()
        for child in self.canvas.children:
            if child.__name__ == "Chart" and child.selected:
                child.set_property('type', type)
                self.canvas.queue_draw()
                break

if __name__ == '__main__':
    def quit(widget, event):
        gtk.main_quit()
        return True

    window = gtk.Window()
    window.set_title(_("Properties panel"))
    window.connect("delete-event", quit)
    properties = Properties(None)
    window.add(properties)
    window.show_all()
    gtk.main()
