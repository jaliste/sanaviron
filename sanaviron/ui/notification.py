#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk

class Notification(gtk.HBox):
    """This class represents a notification bar"""

    def __init__(self):
        gtk.HBox.__init__(self)
        self.set_spacing(3)
        #self.set_border_width(6)

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_MENU)
        self.pack_start(image, False, False)

        self.label = gtk.Label("")
        self.label.set_markup(_("Notification"))
        self.label.set_alignment(0.0, 0.5)
        self.pack_start(self.label, False, False)
        
    def set_text(self, text):
        self.label.set_markup(text)

if __name__ == '__main__':
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    notification = Notification()
    window.add(notification)
    window.show_all()
    gtk.main()
