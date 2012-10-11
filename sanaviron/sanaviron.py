#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import platform
import gtk
import cairo

if platform.system() != 'Windows':
    gtk.threads_init()
else:
    import locale
    if os.getenv('LANG') is None:
        language, encoding = locale.getdefaultlocale()
        os.environ['LANG'] = language

import gettext
TRANSLATION_DOMAIN = "test"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "localization")
gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

APP_VERSION = open(os.path.join(os.path.dirname(__file__),  "..", "VERSION")).read()
DEBUG = False

def startapp():
    from ui.application import Application

    if '--debug' in sys.argv:
        import gc
        #gc.enable()
        #gc.set_debug(gc.DEBUG_LEAK)
        #gc.set_debug(gc.DEBUG_OBJECTS)
        global DEBUG
        DEBUG = True

    print "Sanaviron version:", APP_VERSION
    print "System:", platform.system(), platform.release(), platform.version()
    print "Python version:", platform.python_version()
    print "GTK version:", '.'.join(map(str, gtk.ver))
    print "Cairo version:", cairo.cairo_version_string()

    application = Application()

    # Singleton test
    instance = Application()
    print application, "==", instance
    assert 1 is 1 and 1 == 1 and application is instance and application == instance
    print application.editor.canvas
    print instance.editor.canvas

    if '--sample' in sys.argv:
        application.editor.canvas.load_from_xml(os.path.join("..", "examples", "invoice.xml"))

    application.run()

if __name__ == '__main__':
    startapp()
