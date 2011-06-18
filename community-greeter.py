#!/usr/bin/python
#
# Copyright 2011 Max <govnototalitarizm@gmail.com>
# Copyright 2011 Martin Owens
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
GDM greeter for TAILS project using gtk
"""

import logging
#from gi.repository import Gtk, Gdk, GLib, GObject
import gtk
from gtk import gdk

from gtkme import GtkApp
from GdmGreeter.services import GdmGreeter
#from GdmGreeter.language import ( LanguageWindow, TranslatableWindow, Translatable )
from GdmGreeter.language import ( LanguageWindow, Translatable )
from GdmGreeter.login import LoginWindow
from GdmGreeter.register import RegisterWindow
from GdmGreeter.user import User
from GdmGreeter import GLADE_DIR, __appname__

# Store users and their settings here
USER_CONF = '/home/users/%s.conf'

logging.config.fileConfig('tails-logging.conf')

def print_log_record_on_error(func):
    def wrap(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            import sys
            print >>sys.stderr, "Unable to create log message msg=%r, args=%r " % (getattr(self, 'msg', '?'), getattr(self, 'args', '?'))
            raise
    return wrap

class CommunityGreeterApp(GtkApp, GdmGreeter):
    """Identity Menu for setting up or importing a new identity"""
    app_name  = __appname__
    glade_dir = GLADE_DIR
    windows   = [ LoginWindow, LanguageWindow, RegisterWindow ]

    def __init__(self, *args, **kwargs):
        GtkApp.__init__(self, *args, **kwargs)
        GdmGreeter.__init__(self)
        #self.scr = Gdk.Display.get_default().get_screen(self.display.number)
        self.scr = gdk.display_get_default().get_screen(self.display.number)
        self.lang = None
        #self.lang = 'en'
        self.login = None
        self.user = None
        self.language = 'en_GB.UTF-8'
        self.session = None
        self.layout = None

    def load_window(self, *args, **kwargs):
        """When loading a window, also translate it"""
        window = GtkApp.load_window(self, *args, **kwargs)
        if isinstance(window, Translatable) and self.language:
            logging.debug("Translating %s to %s", (window.name, self.language))
            window.translate_to(self.language)
        return window

    def translate_to(self, lang):
        """Translate all windows to target language"""
        self.language = lang
        for window in self._loaded.values():
            if isinstance(window, Translatable):
                logging.debug("I18n window %s to %s", (window.name, lang))
                window.translate_to(lang)

    def Ready(self):
        """Sever is ready"""
        if not self.lang:
            self.lang = self.load_window('language')
            self.lang.set_position(self.scr.get_width(), self.scr.get_height())
        if not self.login:
            # Load this after language to give it focus
            self.login = self.load_window('login', service=self.obj)
        else:
            self.login.window.set_sensitive(True)
            self.login.show_user('')
        # Tie up the responses, I should do a signal here.
        GdmGreeter.Ready(self)
        logging.warn("server is ready.")

    def SelectedUserChanged(self, username):
        """The user has selected the user to login as"""
        self.user = User(username)
        self.SelectLanguage(self.user.get('language', 'en'), loaded=True)

    def SelectLanguage(self, lang, loaded=False):
        """The user wants to change languages"""
        if not loaded and self.user:
            self.user.save(data={ 'language': lang })
        # Translate all windows in the login screen
        self.translate_to(lang)
        # Make sure the session is set correctly.
        if self.user:
            GdmGreeter.SelectLanguage(self, lang)

    def DefaultLanguageNameChanged(self, lang):
        self.language = lang

    def DefaultLayoutNameChanged(self, layout):
        self.layout = str(layout)

    def DefaultSessionNameChanged(self, session):
        self.session = str(session)

    def InfoQuery(self, text):
        """Server wants to ask the user for something"""
        self.login.show_user(text)

    def SecretInfoQuery(self, text):
        """Server wants to ask for some secrate info"""
        self.login.show_pass(text)

    def FinishProcess(self):
        """We're done, quit gtk app"""
        logging.info("Finished.")
        gtk.main_quit()


if __name__ == "__main__":
    logging.info("Started.")
    app = CommunityGreeterApp()
    gtk.main()
