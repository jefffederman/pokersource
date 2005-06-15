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
        self.game.verbose = 3
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

    def test1(self):
        """
        Five players, they check/call during rounds and start over.

                        Players
        serials     1   2   3   4  5
        seats       0   1   2   3  4
        positions   0   1   2   3  4
        """
        game = self.game
        player = {}
        for serial in xrange(1,6):
            player[serial] = serial - 1
            self.make_new_player(serial)

        #
        # First turn, everyone checks and stays in game
        #
        game.beginTurn(1)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[1]) # dealer
        self.assertEqual(game.last_to_talk, player[3]) # big blind

        for serial in (4, 5, 1, 2):
            self.assertEqual(game.position, player[serial])
            game.call(serial)

        self.assertEqual(game.position, player[3])
        game.check(3) # big blind

        for stage in ("flop", "turn", "river"):
            self.assertEqual(game.state, stage)
            for serial in (2, 3, 4, 5, 1):
                self.assertEqual(game.position, player[serial])
                game.check(serial)
        self.assertEqual(game.state, "end")

        #
        # Second turn, everyone folds games end prematurely
        #
        game.beginTurn(2)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[2]) # dealer
        self.assertEqual(game.last_to_talk, player[4]) # big blind
        for serial in (5, 1, 2, 3):
            self.assertEqual(game.position, player[serial])
            self.assertEqual(game.fold(serial), True)
        self.assertEqual(game.state, "end")
        #
        # Third turn, a new player comes in during the turn, two
        # players in game. The new player is ignored.
        #
        game.beginTurn(3)
        self.make_new_player(6)
        player[6] = 5
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[3]) # dealer
        self.assertEqual(game.last_to_talk, player[5]) # big blind
        self.assertEqual(game.position, player[1])
        game.call(1)
        for serial in (2, 3, 4):
            self.assertEqual(game.position, player[serial])
            game.fold(serial)
        self.assertEqual(game.position, player[5])
        game.check(5)
        for stage in ("flop", "turn", "river"):
            self.assertEqual(game.state, stage)
            self.assertEqual(game.position, player[5]) # next to the dealer is gone, therefore it's the next to him
            for serial in (5, 1):
                self.assertEqual(game.position, player[serial])
                game.check(serial)
        self.assertEqual(game.state, "end")
        #
        # Fourth turn, we now have six players in game, the
        # newcomer pays the big blind
        #
        game.beginTurn(4)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[4]) # dealer
        self.assertEqual(game.last_to_talk, player[6]) # big blind
        self.assertEqual(game.position, player[1])
        game.call(1)
        for serial in (2, 3, 4, 5):
            self.assertEqual(game.position, player[serial])
            game.fold(serial)
        self.assertEqual(game.position, player[6])
        game.check(6)
        for stage in ("flop", "turn", "river"):
            self.assertEqual(game.state, stage)
            self.assertEqual(game.position, player[6]) # next to the dealer is gone, therefore it's the next to him
            for serial in (6, 1):
                self.assertEqual(game.position, player[serial])
                game.check(serial)
        self.assertEqual(game.state, "end")
        #
        # Fifth turn, a player (the dealer) leaves in the middle
        # of the game, auto_play takes over.
        #
        game.beginTurn(5)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[5]) # dealer
        self.assertEqual(game.last_to_talk, player[1]) # big blind
        for serial in (2, 3):
            self.assertEqual(game.position, player[serial])
            game.fold(serial)
        game.removePlayer(5)
        game.autoPlayer(5)
        for serial in (4, 6):
            self.assertEqual(game.position, player[serial])
            game.call(serial)
        self.assertEqual(game.position, player[1])
        game.check(1)
        for stage in ("flop", "turn", "river"):
            self.assertEqual(game.state, stage)
            self.assertEqual(game.last_to_talk, player[4])
            self.assertEqual(game.position, player[6]) # next to the dealer is gone, therefore it's the next to him
            for serial in (6, 1, 4):
                self.assertEqual(game.position, player[serial])
                game.check(serial)
        self.assertEqual(game.state, "end")
        #
        # Sixth turn, everyone folds and game ends prematurely.
        # player[5] is gone for good, discarded at the end of the
        # previous turn.
        #
        player[6] -= 1
        game.beginTurn(6)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[6]) # dealer
        self.assertEqual(game.last_to_talk, player[2]) # big blind
        for serial in (3, 4, 6, 1):
            self.assertEqual(game.position, player[serial])
            game.fold(serial)
        self.assertEqual(game.state, "end")
        #
        # Seventh turn, the dealer passes to player[1] again
        #
        game.beginTurn(7)
        self.assertEqual(game.state, "pre-flop")
        self.assertEqual(game.dealer, player[1]) # dealer
        self.assertEqual(game.last_to_talk, player[3]) # big blind
        for serial in (4, 6, 1, 2):
            self.assertEqual(game.position, player[serial])
            game.fold(serial)
        self.assertEqual(game.state, "end")

    def test2(self):
        """
        getRequestedAction and setPlayerBlind tests
        """
        game = self.game
        for serial in xrange(1,5):
            self.failUnless(game.addPlayer(serial))
            self.failUnless(game.payBuyIn(serial, game.maxBuyIn()))
            self.failUnless(game.sit(serial))
        self.failUnless(game.addPlayer(5))
        self.assertEqual(game.getRequestedAction(5), "buy-in")
        self.failUnless(game.payBuyIn(5, game.maxBuyIn()))
        self.assertEqual(game.getRequestedAction(5), None)
        game.getPlayer(5).money.set(1)
        self.assertEqual(game.getRequestedAction(5), "rebuy")
        self.failUnless(game.rebuy(5, game.buyIn()))
        self.assertEqual(game.getRequestedAction(5), None)
        self.failUnless(game.sit(5))
        #
        # turn 1
        #
        game.beginTurn(8)
        self.assertEqual(game.state, "blindAnte")
        self.assertEqual(game.getRequestedAction(2), "blind_ante")
        (amount, dead, state) = game.blindAmount(2)
        game.blind(2, amount, dead)
        self.assertEqual(game.getRequestedAction(3), "blind_ante")
        (amount, dead, state) = game.blindAmount(3)
        game.blind(3, amount, dead)
        self.assertEqual(game.getRequestedAction(4), "play")
        for serial in xrange(1,6):
            game.botPlayer(serial)
        #
        # turn 2,3,4
        #
        self.failUnless(game.sitOut(4))
        game.beginTurn(9)
        game.beginTurn(10)
        game.beginTurn(11)
        for serial in xrange(1,6):
            game.interactivePlayer(serial)
        #
        # player 4 back in the game must pay the big blind
        #
        self.failUnless(game.sit(4))
        game.beginTurn(12)
        self.assertEqual(game.state, "blindAnte")
        self.assertEqual(game.getRequestedAction(2), "blind_ante")
        (amount, dead, state) = game.blindAmount(2)
        game.blind(2, amount, dead)
        self.assertEqual(game.getRequestedAction(3), "blind_ante")
        (amount, dead, state) = game.blindAmount(3)
        game.blind(3, amount, dead)
        self.assertEqual(game.getRequestedAction(4), "blind_ante")
        game.setPlayerBlind(4, "big_and_dead")
        self.assertEqual(game.getRequestedAction(4), "blind_ante")        

def run():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPosition))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
if __name__ == '__main__':
    run()
