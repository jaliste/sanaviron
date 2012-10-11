"""
___init___.py
"""

__all__ = [ "APP_VERSION", "set_locale", "install_gettext", "print_summary" ]

import platform
import locale
import gettext
import os
import cairo
import gtk

APP_VERSION = open(os.path.join(os.path.dirname(__file__), "VERSION")).read()

def set_locale():
    if os.getenv('LANG') is None:
        LANGUAGE, ENCODING = locale.getdefaultlocale()
        os.environ['LANG'] = LANGUAGE

def install_gettext(domain):
    TRANSLATION_DOMAIN = domain
    LOCALE_DIR = os.path.join(os.path.dirname(__file__), "localization")
    gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

def print_summary():
    print "Sanaviron version:", APP_VERSION
    print "System:", platform.system(), platform.release(), platform.version()
    print "Python version:", platform.python_version()
    print "GTK version:", '.'.join(map(str, gtk.ver))
    print "Cairo version:", cairo.cairo_version_string()
