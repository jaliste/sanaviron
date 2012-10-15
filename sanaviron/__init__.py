"""
___init___.py
"""

__all__ = ["APP_VERSION", "set_locale", "install_gettext", "get_summary"]

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

def get_summary():
    summary = "Sanaviron version: %s\n" % APP_VERSION
    summary += "System: %s %s %s\n" % (platform.system(), platform.release(), platform.version())
    summary += "Python version: %s\n" % platform.python_version()
    summary += "GTK version: %s\n" % '.'.join(map(str, gtk.ver))
    summary += "Cairo version: %s" % cairo.cairo_version_string()

    return summary