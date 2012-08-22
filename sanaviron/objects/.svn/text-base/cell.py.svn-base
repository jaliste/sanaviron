#!/usr/bin/python
# -*- coding: utf-8 -*-


class Cell(Rectangle):
    """This class represents a table cell"""

    def __init__(self):
        Rectangle.__init__(self)
        self.color = Color(0, 0, 0, 1)

        self.size = 18
        self.text = "cell"

    def draw(self, context):
        layout = pangocairo.CairoContext.create_layout(context);
        font = pango.FontDescription("Verdana %d" % self.size)
        layout.set_font_description(font)
        layout.set_markup(self.text)

        context.set_source_rgba(self.color.red, self.color.green,
            self.color.blue, self.color.alpha)

        width, height = layout.get_size()
        width /= pango.SCALE
        height /= pango.SCALE

        context.move_to(self.x, self.y)
        context.show_layout(layout)

        dash = [5.0, 3.0]
        context.set_dash(dash)
        context.set_line_width(0.5)
        context.rectangle(self.x, self.y, self.width, self.height)
        #context.set_source_rgba(self.red, self.green, self.blue, self.alpha)
        #context.fill_preserve()
        context.set_source_rgba(self.color.red, self.color.green,
            self.color.blue, self.color.alpha)
        context.stroke()
