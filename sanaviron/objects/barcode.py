#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import pango
import pangocairo
from ctypes import c_char_p, c_int, c_double, CDLL
from object import Object
from objects import *

BARCODE_ANY = 0  # /* Choose best-fit */
BARCODE_EAN = 1  # /* Code EAN */
BARCODE_UPC = 2  # /* UPC = 12-digit EAN */
BARCODE_ISBN = 3  # /* ISBN numbers (still EAN13) */
BARCODE_39 = 4  # /* Code 39 */
BARCODE_128 = 5  # /* Code 128 (a = b = c: autoselection) */
BARCODE_128C = 6  # /* Code 128 (compact form for digits) */
BARCODE_128B = 7  # /* Code 128 =  full printable ASCII */
BARCODE_I25 = 8  # /* Interleaved 2 of 5 (only digits) */
BARCODE_128RAW = 9  # /* Raw code 128 (by Leonid A. Broukhis) */
BARCODE_CBR = 10 # /* Codabar (by Leonid A. Broukhis) */
BARCODE_MSI = 11 # /* MSI (by Leonid A. Broukhis) */
BARCODE_PLS = 12 # /* Plessey (by Leonid A. Broukhis) */
BARCODE_93 = 13 # /* Code 93 (by Nathan D. Holmes) */
POSTNET = 14 # /* Any of 5, 9 or 11 digits POSTNET */
POSTNET_5 = 15 # /* 5 digits POSTNET */
POSTNET_6 = 16 # /* 5 digits POSTNET */
POSTNET_9 = 17 # /* 9 digits POSTNET */
POSTNET_11 = 18 # /* 11 digits POSTNET */
CEPNET = 19 # /* 11 digits POSTNET */
DATAMATRIX = 20 # /* 2D data matrix ECC200 ISO/IEC16022 */
QR = 21 # /* 2D QR */

barcodes = {
    _("Choose best-fit"): BARCODE_ANY,
    _("Code EAN"): BARCODE_EAN,
    _("UPC"): BARCODE_UPC,
    _("ISBN"): BARCODE_ISBN,
    _("Code 39"): BARCODE_39,
    _("Code 128"): BARCODE_128,
    _("Code 128C"): BARCODE_128C,
    _("Code 128B"): BARCODE_128B,
    _("Interleaved 2 of 5"): BARCODE_I25,
    _("Raw code 128"): BARCODE_128RAW,
    _("Codabar"): BARCODE_CBR,
    _("MSI"): BARCODE_MSI,
    _("Plessey"): BARCODE_PLS,
    _("Code 93"): BARCODE_93,
    _("POSTNET"): POSTNET,
    _("POSTNET 5"): POSTNET_5,
    _("POSTNET 6"): POSTNET_6,
    _("POSTNET 9"): POSTNET_9,
    _("POSTNET 11"): POSTNET_11,
    _("CEPNET"): CEPNET,
    _("Data matrix"): DATAMATRIX,
    _("QR"): QR
}

if platform.system() == "Windows":
    extension = "dll"
else:
    extension = "so"

if platform.machine() == "x86_64":
    suffix = platform.machine() + "."
else:
    suffix = ""

BCIface = CDLL(os.path.join(os.path.dirname(__file__), "barcode", "barcode." + suffix + extension))

BCIface.get_code_data.argtypes = (c_int, c_char_p, c_double, c_double)
BCIface.get_code_data.restype = c_char_p
BCIface.get_text_data.restype = c_char_p

DEFAULT_CODE_TYPE = BARCODE_39

class BarCode(Object):
    """This class represents a barcode"""

    __name__ = "BarCode"

    def __init__(self, code="800894002700", barcode_type=DEFAULT_CODE_TYPE):
        Object.__init__(self)

        self.code = code
        self.type = barcode_type

    def get_properties(self):
        return Object.get_properties(self) + ["code", "type"]

    def post(self):
        self.handler.control[NORTHWEST].x = self.x
        self.handler.control[NORTHWEST].y = self.y
        self.handler.control[NORTHEAST].x = self.x + self.width
        self.handler.control[NORTHEAST].y = self.y
        self.handler.control[SOUTHWEST].x = self.x
        self.handler.control[SOUTHWEST].y = self.y + self.height
        self.handler.control[SOUTHEAST].x = self.x + self.width
        self.handler.control[SOUTHEAST].y = self.y + self.height
        self.handler.control[NORTH].x = self.x + self.width / 2
        self.handler.control[NORTH].y = self.y
        self.handler.control[SOUTH].x = self.x + self.width / 2
        self.handler.control[SOUTH].y = self.y + self.height
        self.handler.control[WEST].x = self.x
        self.handler.control[WEST].y = self.y + self.height / 2
        self.handler.control[EAST].x = self.x + self.width
        self.handler.control[EAST].y = self.y + self.height / 2

        if int(self.type) in [DATAMATRIX, QR]:
            self.handler.control[NORTH].active = False
            self.handler.control[SOUTH].active = False
            self.handler.control[WEST].active = False
            self.handler.control[EAST].active = False
            self.handler.can_pivot = False
            if self.width != self.height:
                size = max(self.width, self.height)
                self.width = self.height = size
        else:
            self.handler.control[NORTH].active = True
            self.handler.control[SOUTH].active = True
            self.handler.control[WEST].active = True
            self.handler.control[EAST].active = True
            self.handler.can_pivot = True

    def draw(self, context):
        code = str(self.code)
        type = int(self.type)
        description = "Verdana 12"

        data = BCIface.get_code_data(type, code, self.width, self.height)
        text = BCIface.get_text_data(type, code)

        if not data:
            context.rectangle(self.x, self.y, self.width, self.height)
            context.set_source_rgba(0.75, 0, 0, 0.25)
            context.fill_preserve()
            context.set_source_rgb(0.75, 0, 0)
            context.set_line_width(4.0)
            context.set_dash([])
            context.stroke()

            margin = 10

            if not code:
                code = _("empty")
                message = _("Please enter a valid code")
            else:
                message = _("Please select another one")
            text = _("Code <b>%(code)s</b> can't\n"
                     "be displayed in this codification.\n"
                     "%(message)s.") % {"code": code, "message": message}

            context = pangocairo.CairoContext(context)
            layout = pangocairo.CairoContext.create_layout(context)
            font = pango.FontDescription(description)
            layout.set_font_description(font)
            layout.set_alignment(pango.ALIGN_CENTER)
            layout.set_markup(text)
            width, height = layout.get_size()
            width /= pango.SCALE
            height /= pango.SCALE
            width += 2 * margin
            height += 2 * margin
            horizontal = self.width / float(width)
            vertical = self.height / float(height)
            context.move_to(self.x + margin, self.y + margin)
            context.save()
            if horizontal and vertical:
                context.scale(horizontal, vertical)
                context.show_layout(layout)
            context.restore()
            Object.draw(self, context)
            return

        context.set_dash([])
        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)

        data = data.split(' ')
        ratio = float(data.pop().replace(',', '.'))

        def get_bar_data(bar):
            x, y, thickness, length = bar.replace(',', '.').split(':')
            return float(x) + self.x, float(y) + self.y, float(thickness), float(length)

        for bar in data:
            x, y, thickness, length = get_bar_data(bar)
            context.move_to(x, y)
            context.line_to(x, y + length)
            context.set_line_width(thickness)
            context.stroke()
            #context.rectangle(x, y, thickness, length)
            #context.fill()

        if text:
            #from:int svg_text(struct Barcode_Item *bc, FILE *f)
            context = pangocairo.CairoContext(context)

            correction = 0 # /* This correction seems to be needed to align text properly */
            px = 0

            text = text.split(' ')

            for digit in text:
                if not len(digit):
                    continue

                i, j, digit = digit.replace(',', '.').split(':')

                x = float(i)

                if (x - px) >= 10:
                    correction += 2
                px = x

                layout = pangocairo.CairoContext.create_layout(context)
                font = pango.FontDescription(description)
                layout.set_font_description(font)
                layout.set_text(digit)
                width, height = layout.get_size()
                height /= pango.SCALE
                context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
                    self.stroke_color.blue, self.stroke_color.alpha)
                context.move_to(self.x + (x * ratio - correction), self.y + self.height - height)
                context.show_layout(layout)

        Object.draw(self, context)

    def resize(self, x, y):
        Object.resize(self, x, y)

        if int(self.type) in [DATAMATRIX, QR]:
            size = max(self.width, self.height)
            self.width = self.height = size

if __name__ == "__main__":
    data = BCIface.get_code_data(BARCODE_EAN, "800894002700", 100, 100)
    text = BCIface.get_text_data(BARCODE_EAN, "800894002700")
    print data, text
