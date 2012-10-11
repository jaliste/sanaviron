#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import platform
from __init__ import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if platform.system() == 'Windows':
    set_locale()
else:
    gtk.threads_init()

install_gettext("sanaviron")

def startapp():
    if '--debug' in sys.argv:
        import gc
        gc.enable()
        gc.set_debug(gc.DEBUG_LEAK)

    print_summary()

    from ui.application import Application
    application = Application()

    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("..", "examples", "invoice.xml"))

    application.run()

if __name__ == '__main__':
    startapp()