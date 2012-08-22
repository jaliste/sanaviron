#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import gtk

# TODO: Browser to Engine.

if os.name == 'posix':
    #import gtkmozembed

    #class Browser(gtkmozembed.MozEmbed):

    class Browser:
        def __init__(self, url):
            #gtkmozembed.MozEmbed.__init__(self)
            self.load_url(url)

        def load_url(self, url):
            pass

else:
    WS_VISIBLE = 0x10000000
    WS_CHILD = 0x40000000
    # TODO: Use GtkScrolledWindow instead
    WS_VSCROLL = 0x00200000
    WS_HSCROLL = 0x00100000

    #WS_OVERLAPPED   = 0x00000000
    #WS_POPUP        = 0x80000000
    #WS_CHILD        = 0x40000000
    #WS_MINIMIZE     = 0x20000000
    #WS_VISIBLE      = 0x10000000
    #WS_DISABLED     = 0x08000000
    #WS_CLIPSIBLINGS = 0x04000000
    #WS_CLIPCHILDREN = 0x02000000
    #WS_MAXIMIZE     = 0x01000000
    #WS_CAPTION      = 0x00C00000
    #WS_BORDER       = 0x00800000
    #WS_DLGFRAME     = 0x00400000
    #WS_VSCROLL      = 0x00200000
    #WS_HSCROLL      = 0x00100000
    #WS_SYSMENU      = 0x00080000
    #WS_THICKFRAME   = 0x00040000
    #WS_GROUP        = 0x00020000
    #WS_TABSTOP      = 0x00010000
    #WS_MINIMIZEBOX  = 0x00020000
    #WS_MAXIMIZEBOX  = 0x00010000

    from ctypes import *
    from ctypes.wintypes import *

    class Browser(gtk.DrawingArea):
        """This class represents a portable browser for help files"""

        def __init__(self, url):
            gtk.DrawingArea.__init__(self)

            self.connect("realize", self.realized)

        def realized(self, widget):
            kernel32 = windll.kernel32
            user32 = windll.user32
            atl = windll.atl

            def on_container_size(widget, sizeAlloc, gtkAtlAxWin):
                gtkAtlAxWin.move_resize(0, 0, sizeAlloc.width, sizeAlloc.height)

            # Make the container accept the focus and pass it to the control;
            # this makes the Tab key pass focus to IE correctly.
            #self.set_property("can-focus", True)
            #self.connect("focus", on_container_focus)

            # Create an instance of IE via AtlAxWin.
            atl.AtlAxWinInit()
            hInstance = kernel32.GetModuleHandleA(None)
            parentHwnd = self.window.handle
            atlAxWinHwnd = user32.CreateWindowExA(0, "AtlAxWin", url,
                WS_VISIBLE | WS_CHILD | WS_HSCROLL | WS_VSCROLL,
                0, 0, 100, 100, parentHwnd, None, hInstance, 0)

            # Get the IWebBrowser2 interface for the IE control.
            #pBrowserUnk = POINTER(IUnknown)()
            #atl.AtlAxGetControl(atlAxWinHwnd, byref(pBrowserUnk))
            #pBrowser = POINTER(IWebBrowser2)()
            #pBrowserUnk.QueryInterface(byref(IWebBrowser2._iid_), byref(pBrowser))

            # Create a Gtk window that refers to the native AtlAxWin window.
            gtkAtlAxWin = gtk.gdk.window_foreign_new(long(atlAxWinHwnd))

            # Resize the AtlAxWin window with its container.
            self.connect("size-allocate", on_container_size, gtkAtlAxWin)

            # By default, clicking a GTK widget doesn't grab the focus away from
            # a native Win32 control.
            #test_entry.connect("button-press-event", self.on_widget_click)

            #    def on_goButton_clicked(self, widget):
            #        v = byref(VARIANT())
            #        self.pBrowser.Navigate(self.addressEntry.get_text(), v, v, v, v)
            #
            #    def on_addressEntry_key(self, widget, event):
            #        if event.keyval == 65293:   # "Enter"; is there a constant for this?
            #            self.on_goButton_clicked(None)
            #
            #    def on_widget_click(self, widget, data):
            #        self.main.window.focus()
            #
            #    def on_container_size(self, widget, sizeAlloc):
            #        self.gtkAtlAxWin.move_resize(0, 0, sizeAlloc.width, sizeAlloc.height)
            #
            #    def on_container_focus(self, widget, data):
            #        # Pass the focus to IE.  First get the HWND of the IE control; this
            #        # is a bit of a hack but I couldn't make IWebBrowser2._get_HWND work.
            #        rect = RECT()
            #        user32.GetWindowRect(self.atlAxWinHwnd, byref(rect))
            #        ieHwnd = user32.WindowFromPoint(POINT(rect.left, rect.top))
            #        user32.SetFocus(ieHwnd)

# TODO: Browser class here.

if __name__ == "__main__":
    # main gtk+ window
    window = gtk.Window()
    window.set_title(_("Portable browser"))
    window.connect("destroy", gtk.main_quit)
    window.set_size_request(750, 550)
    cwd = os.getcwd()
    url = "file://" + cwd + "/help/index.html"
    browser = Browser(url)
    window.add(browser)
    window.show_all()
    gtk.main()
