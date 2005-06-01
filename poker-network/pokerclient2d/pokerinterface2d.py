#
# Copyright (C) 2005 Mekensleep
#
# Mekensleep
# 24 rue vieille du temple
# 75004 Paris
#       licensing@mekensleep.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#  Loic Dachary <loic@gnu.org>
#
import sys
sys.path.insert(0, "..")

import gtk
from pokerclient2d import cpokerinterface
from pokerui.pokerinterface import PokerInterface

class PokerInterface2D(PokerInterface):

    def __init__(self, settings):
        PokerInterface.__init__(self)
        self.verbose = settings.headerGetInt("/settings/@verbose")
        datadir = settings.headerGet("/settings/data/@path")
        cpokerinterface.init(callback = self.event,
                            datadir = datadir,
                            gtkrc = datadir + "/interface/gtkrc",
                            glade = datadir + "/interface/interface2d.glade",
                            verbose = self.verbose,
                            )
        self.width = settings.headerGetInt("/settings/screen/@width")
        self.height = settings.headerGetInt("/settings/screen/@height")
        window = gtk.Window()
        window.set_default_size(self.width, self.height)
        window.set_title("Poker")
        window.set_name("lobby_window_root")
        self.screen = gtk.Layout()
        self.screen.set_size(self.width, self.height)
        self.screen.set_name("screen")
        window.add(self.screen)
        window.show_all()
        
    def __del__(self):
        cpokerinterface.uninit()

    def command(self, *args):
        if self.verbose > 2: print "PokerInterface2D.command: " + str(args)
        cpokerinterface.command(self.screen, *args)
