#
# Copyright (C) 2004 Mekensleep
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

import sys, os
sys.path.insert(0, "..")

import unittest
from pokerengine.pokergame import PokerGameServer

class TestBuyIn(unittest.TestCase):

    def setUp(self):
        self.game = PokerGameServer("poker.%s.xml", [ "../conf" ])
        self.game.verbose = 3
        self.game.setVariant("holdem")
        self.game.setBettingStructure("2-4-limit")

    def tearDown(self):
        del self.game

    def log(self, string):
        print string

    def make_new_player(self, serial, seat):
        game = self.game
        self.failUnless(game.addPlayer(serial, seat))
        self.failUnless(game.payBuyIn(serial, game.buyIn()))
        self.failUnless(game.sit(serial))
        game.botPlayer(serial)
        game.noAutoBlindAnte(serial)

    def pay_blinds(self):
        game = self.game
        for serial in game.serialsAll():
            game.autoBlindAnte(serial)
        for serial in game.serialsAll():
            game.noAutoBlindAnte(serial)

    def test1(self):
        game = self.game
        self.failUnless(game.addPlayer(1))
        self.failIf(game.payBuyIn(1, game.buyIn() - 1))
        self.failIf(game.getPlayer(1).buy_in_payed)
        self.failIf(game.payBuyIn(1, game.maxBuyIn() + 1))
        self.failIf(game.getPlayer(1).buy_in_payed)
        self.failUnless(game.payBuyIn(1, game.buyIn()))
        self.failUnless(game.getPlayer(1).buy_in_payed)

        self.failUnless(game.addPlayer(2))
        self.failUnless(game.payBuyIn(2, game.maxBuyIn()))
        self.failUnless(game.getPlayer(2).buy_in_payed)

    def test2(self):
        for (serial, seat) in ((1, 0), (2, 1), (3, 2), (4, 3)):
            self.make_new_player(serial, seat)
        self.game.beginTurn(1)
        self.failIf(self.game.rebuy(3000, self.game.buyIn()))
        self.failUnless(self.game.rebuy(1, 1))
        self.assertEqual(self.game.getPlayer(1).rebuy, 1)
        self.failIf(self.game.rebuy(1, self.game.maxBuyIn()))
        self.assertEqual(self.game.getPlayer(1).rebuy, 1)
        self.failUnless(self.game.rebuy(1, 1))
        self.assertEqual(self.game.getPlayer(1).rebuy, 2)
        self.pay_blinds()
        self.assertEqual(self.game.getPlayer(1).rebuy, 0)
        money = self.game.getPlayerMoney(1)
        self.failUnless(self.game.rebuy(1, 1))
        self.assertEqual(self.game.getPlayerMoney(1), money + 1)

def run():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBuyIn))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    run()
