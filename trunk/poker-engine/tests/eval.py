#
# Copyright (C) 2004, 2005 Mekensleep
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors:
#  Loic Dachary <loic@gnu.org>
#

import sys, os
sys.path.insert(0, "..")

import unittest
from pokerengine.pokergame import PokerGameServer, PokerGameClient, PokerGame
from pokerengine.pokerchips import PokerChips
from pokerengine.pokercards import PokerCards
from pokereval import PokerEval

poker_eval = PokerEval()
_initial_money = 10

class TestPosition(unittest.TestCase):

    def setUp(self):
        self.game = PokerGameServer("poker.%s.xml", [ "../conf" ])
        self.game.setVariant("holdem")
        self.game.setBettingStructure("2-4-limit")

    def tearDown(self):
        del self.game

    def log(self, string):
        print string

    def make_cards(self, *args):
        return PokerCards(poker_eval.string2card(args))
    
    def make_new_player(self, i, initial_money = _initial_money):
        self.assert_(self.game.addPlayer(i))
        player = self.game.serial2player[i]
        player.money = PokerChips(self.game.chips_values, initial_money)
        player.buy_in_payed = True
        self.assert_(self.game.sit(i))
        player.auto_blind_ante = True

    def make_cards(self, *args):
        return PokerCards(poker_eval.string2card(args))

    def test1(self):
        """
        """
        game = self.game
        player = {}
        for serial in xrange(1,6):
            self.make_new_player(serial)
            player[serial] = game.serial2player[serial]

        game.beginTurn(1)
        for serial in (2, 3, 4, 5):
            player[serial].hand = self.make_cards('__', '__')
        player[1].hand = self.make_cards('Ad', 'As')
        self.assertEqual(game.handEV(1, 10000), 559)
        player[1].hand = self.make_cards('2c', '7s')
        self.assertEqual(game.handEV(1, 10000), 102)

        game.board = self.make_cards('2c', '3c', '4s')
        player[1].hand = self.make_cards('2s', '7s')
        self.assertEqual(game.handEV(1, 10000), 172)

        game.board = self.make_cards('2c', '3c', '4s', '4c')
        player[1].hand = self.make_cards('2s', '7s')
        self.assertEqual(game.handEV(1, 10000), 75)

        game.board = self.make_cards('2c', '3c', '4s', '4c', 'Kc')
        player[1].hand = self.make_cards('2s', '7s')
        self.assertEqual(game.handEV(1, 10000), 5)

def run():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPosition))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    run()
