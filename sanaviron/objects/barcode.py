#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import pango
import pangocairo
from ctypes import c_char_p, CDLL
from object import Object
from objects import *

BARCODE_DEFAULT_FLAGS = 0x00000000
BARCODE_ENCODING_MASK = 0x000000ff # /* 256 possibilites... */
BARCODE_NO_ASCII = 0x00000100 # /* avoid text in output */
BARCODE_NO_CHECKSUM = 0x00000200 # /* avoid checksum in output */
BARCODE_OUTPUT_MASK = 0x000ff000 # /* 256 output types */
BARCODE_OUT_EPS = 0x00001000
BARCODE_OUT_PS = 0x00002000
BARCODE_OUT_PCL = 0x00004000 # /* by Andrea Scopece */
BARCODE_PCL_III = 0x00008000 # /* no idea */
BARCODE_OUT_PCL_III = 0x0000C000
BARCODE_OUT_NOHEADERS = 0x00100000 # /* no header nor footer */

BARCODE_ANY = 0  # /* choose best-fit */
BARCODE_EAN = 1  # /* code ean */
BARCODE_UPC = 2  # /* upc = 12-digit ean */
BARCODE_ISBN = 3  # /* isbn numbers (still EAN13) */
BARCODE_39 = 4  # /* code 39 */
BARCODE_128 = 5  # /* code 128 (a = b = c: autoselection) */
BARCODE_128C = 6  # /* code 128 (compact form for digits) */
BARCODE_128B = 7  # /* code 128 =  full printable ascii */
BARCODE_I25 = 8  # /* interleaved 2 of 5 (only digits) */
BARCODE_128RAW = 9  # /* raw code 128 (by Leonid A. Broukhis) */
BARCODE_CBR = 10 # /* codabar (by Leonid A. Broukhis) */
BARCODE_MSI = 11 # /* msi (by Leonid A. Broukhis) */
BARCODE_PLS = 12 # /* plessey (by Leonid A. Broukhis) */
BARCODE_93 = 13 # /* code 93 (by Nathan D. Holmes) */

barcodes = {
    #"Seleccionar el más adecuado"                                     : BARCODE_ANY,
    #"Codificación EAN"                                                : BARCODE_EAN,
    #"Codificación UPC (EAN de 12 dígitos)"                            : BARCODE_UPC,
    #"Codificación ISBN (números still? EAN13)"                        : BARCODE_ISBN,
    #"Codificación 39"                                                 : BARCODE_ISBN,
    #"Codificación 128 (a = b = c: autoselección)"                     : BARCODE_128,
    #"Codificación 128C (forma compacta para números)"                 : BARCODE_128C,
    #"Codificación 128B (todos los ASCII)"                             : BARCODE_128B,
    #"Codificación I25 (entrelazado 2 de 5, sólo números)"             : BARCODE_I25,
    #"Codificación cruda de 128 (128RAW de Leonid A. Broukhis)"        : BARCODE_128RAW,
    #"Codificación CBR (Codabar de Leonid A. Broukhis)"                : BARCODE_CBR,
    #"Codificación MSI (MSI de Leonid A. Broukhis)"                    : BARCODE_MSI,
    #"Codificación PLS (Plesser de Leonid A. Broukhis)"                : BARCODE_PLS,
    #"Codificación 93 (codificación 39 mejorada por Nathan D. Holmes)" : BARCODE_93
    _("Choose best-fit"): BARCODE_ANY,
    _("Code EAN"): BARCODE_EAN,
    _("UPC"): BARCODE_UPC,
    _("ISBN"): BARCODE_ISBN,
    _("Code 39"): BARCODE_ISBN,
    _("Code 128"): BARCODE_128,
    _("Code 128C"): BARCODE_128C,
    _("Code 128B"): BARCODE_128B,
    _("Interleaved 2 of 5"): BARCODE_I25,
    _("Raw code 128"): BARCODE_128RAW,
    _("Codabar"): BARCODE_CBR,
    _("MSI"): BARCODE_MSI,
    _("Plessey"): BARCODE_PLS,
    _("Code 93"): BARCODE_93
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

BCIface.get_partial.restype = c_char_p
BCIface.get_textinfo.restype = c_char_p

DEFAULT_CODE_TYPE = BARCODE_39

class BarCode(Object):
    """This class represents a barcode"""

    __name__ = "BarCode"

    def __init__(self, code="800894002700", type=DEFAULT_CODE_TYPE):
        Object.__init__(self)
        #self.code = code
        #self.type = type

        self.set_property('code', code)
        self.set_property('type', type)

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

    def draw(self, context):
        code = self.get_property('code')
        type = self.get_property('type')

        partial = BCIface.get_partial(type, code)
        textinfo = BCIface.get_textinfo(type, code)

        if not partial:
            return

        #from:int svg_bars(struct Barcode_Item *bc, FILE *f)
        count = len(partial)
        i = 0     # /* Loop counter */
        x = 0     # /* Where the current box is drawn */
        #is_bar = False

        while i < count:
            current = ord(partial[i]) - 48

            if current > 9:
                if i + 1 >= count:
                    break
                current = ord(partial[i + 1]) - 48
                i += 2      # /* Skip the following 'a' */
                #else:
            #  height = self.height - 20

            x += current
            i += 1

        ratio = self.width / x
        i = 0     # /* Loop counter */
        x = 0     # /* Where the current box is drawn */
        is_bar = False

        while i < count:
            current = ord(partial[i]) - 48

            if current > 9:
                height = self.height # /* Guide bar */
                if i + 1 >= count:
                    break
                current = ord(partial[i + 1]) - 48
                i += 2      # /* Skip the following 'a' */
            else:
                height = self.height - 20

            if is_bar:
                context.rectangle(self.x + x, self.y, current * ratio, height)
                is_bar = False
            else:
                is_bar = True

            x += current * ratio
            #x += current
            i += 1

        context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
            self.stroke_color.blue, self.stroke_color.alpha)
        context.fill()
        #context.fill_preserve()
        #context.stroke()

        #from:int svg_text(struct Barcode_Item *bc, FILE *f)
        context = pangocairo.CairoContext(context)

        correction = 0 # /* This correction seems to be needed to align text properly */
        description = "Verdana 12"
        #x = 0
        px = 0
        #d = 0.0

        for digit in textinfo.split(' '):
            if not len(digit):
                continue

            i, j, text = digit.split(':')

            try:
                x = int(i)
            except:
                return # TODO

            if (x - px) >= 10:
                correction += 2
            px = x

            layout = pangocairo.CairoContext.create_layout(context)
            font = pango.FontDescription(description)
            layout.set_font_description(font)
            layout.set_markup(text)
            width, height = layout.get_size()
            height /= pango.SCALE
            context.set_source_rgba(self.stroke_color.red, self.stroke_color.green,
                self.stroke_color.blue, self.stroke_color.alpha)
            context.move_to(self.x + (x * ratio - correction), self.y + self.height - height)
            context.show_layout(layout)

            Object.draw(self, context)


if __name__ == "__main__":
    partial = BCIface.get_partial(BARCODE_EAN, "800894002700")
    textinfo = BCIface.get_textinfo(BARCODE_EAN, "800894002700")
    print partial
    print textinfo
