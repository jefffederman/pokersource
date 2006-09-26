#!/usr/bin/python2.4
# -*- mode: python -*-
#
# Copyright (C) 2006 Mekensleep
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
#  Cedric Pinson <cpinson@freesheep.org>
# 

import sys, os
sys.path.insert(0, "./..")
sys.path.insert(0, "..")

from pokerui.pokerrenderer import PokerRenderer
from pokerui.pokerrenderer import  LEAVING_DONE, CANCELED, SIT_OUT, LEAVING, LEAVING_CONFIRM, JOINING, JOINING_MY, REBUY, PAY_BLIND_ANTE, PAY_BLIND_ANTE_SEND, MUCK, USER_INFO, HAND_LIST, SEARCHING_MY_CANCEL, SEARCHING_MY, LOBBY, IDLE, OUTFIT, QUIT, CASHIER, QUIT_DONE, TOURNAMENTS, TOURNAMENTS_REGISTER, TOURNAMENTS_UNREGISTER,  SEATING, LOGIN, BUY_IN
from pokerui.pokerinterface import INTERFACE_YESNO
from pokernetwork.packets import PacketQuit, PacketSerial, PACKET_QUIT
from pokernetwork.pokerpackets import PacketPokerId, PACKET_POKER_GET_PERSONAL_INFO, PACKET_POKER_GET_USER_INFO

import unittest

#-----------------
class PokerInteractorsMockup:
    def __init__(self):
        self.call_destroy = False

    def destroy(self):
        self.call_destroy = True

class PokerRendererMockup(PokerRenderer):
    def __init__(self):
	self.factory = PokerFactoryMockup()
	self.verbose = 3
	self.protocol = PokerProtocolMockup()
        self.state = IDLE
        self.stream_mode = True
        self.state_outfit = None
        self.interactors = PokerInteractorsMockup()
        self.send_packet = None
        self.call_showYesNo = False
        self.call_hideYesNo = False
        self.quit_state = None
        self.change_state = []
        self.call_hideTournaments = False
        self.call_hideLobby = False
        self.call_showLobby = False
        self.call_hideTournaments = False
        self.call_showTournaments = False
        self.call_hideHands = False
        self.call_hideMuck = False
        self.call_hideCashier = False
        self.call_showCashier = False
        self.call_showOutfit = False
        self.call_hideOutfit = False
        self.call_showMessage = False
        self.call_requestBuyIn = False
        self.state_hands = {}
        self.call_showHands = False
        self.call_hideHands = False
        self.call_queryHands = False
        self.call_postMuck = False
        self.call_showMuck = False
        self.call_payAnte = False
        self.call_payBlind = False
        self.call_hideBuyIn = False
        self.call_sitActionsHide = False

    def isSeated(self):
        return False

    def sitActionsHide(self):
        self.call_sitActionsHide = True

    def hideBuyIn(self):
        self.call_hideBuyIn = True

    def payAnte(self, arg):
        self.call_payAnte = True

    def payBlind(self, arg):
        self.call_payBlind = True

    def postMuck(self, arg):
        self.call_postMuck = True

    def showMuck(self, arg):
        self.call_showMuck = True

    def queryHands(self):
        self.call_queryHands = True

    def requestBuyIn(self, game):
        self.call_requestBuyIn = True
        return True

    def showHands(self):
        self.call_showHands = True

    def hideHands(self):
        self.call_hideHands = False
        
    def hideLobby(self):
        self.call_hideLobby = True

    def showMessage(self, msg, dummy):
        self.call_showMessage = msg

    def showTournaments(self):
        self.call_showTournaments = True

    def hideTournaments(self):
        self.call_hideTournaments = True

    def showOutfit(self):
        self.call_showOutfit = True

    def hideCashier(self):
        self.call_hideCashier = True

    def showCashier(self):
        self.call_showCashier = True

    def hideOutfit(self):
        self.call_hideOutfit = True

    def showLobby(self):
        self.call_showLobby = True

    def hideMuck(self):
        self.call_hideMuck = True
        
    def showYesNoBox(self, msg):
        self.call_showYesNo = True;

    def hideHands(self):
        self.call_hideHands = True;

    def hideYesNoBox(self):
        self.call_hideYesNo = True;

    def sendPacket(self, packet):
        self.send_packet = packet

    def queryTournaments(self):
        pass

    def queryLobby(self):
        pass

    def chatHide(self):
        pass
        
    def render(self, packet):
        print "render packet %s" % str(packet)

    def changeState(self, state, *args, **kwargs):
        self.change_state.append((self.state, state))
        PokerRenderer.changeState(self, state, *args, **kwargs)

class PokerUserMockup:
    def __init__(self):
        pass

    def isLogged(self):
        return True
        
class PokerProtocolMockup:
    def __init__(self):
	self.packets = []
        self.user = PokerUserMockup()
        self.send_packet = None
        
    def schedulePacket(self, packet):
	self.packets.append(packet)

    def sendPacket(self, packet):
        self.send_packet = packet

    def getSerial(self):
        return 0
        
class PokerInterfaceMockup:
    def __init__(self):
	self.verbose = 3
        self.callbacks = {}

    def showMenu(self):
        pass

    def hideMenu(self):
        pass
    
    def chatShow(self):
        pass

    def registerHandler(self, key, func):
        self.callbacks[key] = func

class PokerSettingMockup:
    def __init__(self):
        pass

    def headerGet(self, path):
        return "yes"
    
class PokerFactoryMockup:
    def __init__(self):
	self.verbose = 3
	self.chat_config = {'max_chars': 80,
			    'line_length': 80}
        self.interface = PokerInterfaceMockup()
        self.call_quit = False
        self.call_getGame = False
        self.settings = PokerSettingMockup()

    def quit(self):
        self.call_quit = True

    def getGame(self, id):
        self.call_getGame = True
        return 0
        
class PokerPacketChatMockup:
    def __init__(self, message):
	self.message = message
	self.serial = 0
	self.game_id = 0

class PokerRendererTestCase(unittest.TestCase):
    
    # -----------------------------------------------------------------------------------------------------
    def setUp(self):
	self.renderer = PokerRendererMockup()
    
    # -----------------------------------------------------------------------------------------------------    
    def tearDown(self):
	self.renderer = None
        
    # -----------------------------------------------------------------------------------------------------    
    def test_StateQUITFromOUTFIT(self):
        self.renderer.state = OUTFIT
	self.assertEquals(self.renderer.state, OUTFIT)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, LOBBY)
	self.assertEquals(self.renderer.call_hideOutfit, True)

    def test_StateOUTFITFromQUITFromLOBBY(self):
        self.renderer.quit_state = LOBBY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOBBY)
        self.renderer.changeState(OUTFIT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, OUTFIT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,OUTFIT))
        self.assertEquals(self.renderer.change_state[1], (LOBBY,OUTFIT))
	self.assertEquals(self.renderer.call_showOutfit, True)


    # -----------------------------------------------------------------------------------------------------    
    def test_StateQUITFromIDLE_Without_INTERFACE(self):
        self.renderer.state = IDLE
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, IDLE)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromIDLE_COMMON(self):
        self.renderer.state = IDLE
	self.assertEquals(self.renderer.state, IDLE)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)

    def test_StateQUITFromIDLE_YES(self):
        self.test_StateQUITFromIDLE_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        
    def test_StateQUITFromIDLE_NO(self):
        self.test_StateQUITFromIDLE_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, IDLE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateIDLEFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(IDLE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,IDLE))
        self.assertEquals(self.renderer.change_state[1], (IDLE,IDLE))

    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromLOBBY_Without_INTERFACE(self):
        self.renderer.state = LOBBY
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, LOBBY)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLOBBY_COMMON(self):
        self.renderer.state = LOBBY
	self.assertEquals(self.renderer.state, LOBBY)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOBBY)

    def test_StateQUITFromLOBBY_NO(self):
        self.test_StateQUITFromLOBBY_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, LOBBY)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLOBBY_YES(self):
        self.test_StateQUITFromLOBBY_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, LOBBY)

    def test_StateLOBBYFromQUITFromLOBBY(self):
        self.renderer.quit_state = LOBBY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOBBY)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (LOBBY,LOBBY))

    # -----------------------------------------------------------------------------------------------------    

    def test_StateLOBBYFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,LOBBY))
        self.assertEquals(self.renderer.call_hideTournaments, True)
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (SEATING,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (IDLE,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (REBUY,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (MUCK,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, True)

    def test_StateLOBBYFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)


    def test_StateLOBBYFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (JOINING,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)

    def test_StateLOBBYFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(LOBBY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOBBY))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,LOBBY))
        self.assertEquals(self.renderer.call_showLobby, False)
    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromTOURNAMENTS_Without_INTERFACE(self):
        self.renderer.state = TOURNAMENTS
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, TOURNAMENTS)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_COMMON(self):
        self.renderer.state = TOURNAMENTS
	self.assertEquals(self.renderer.state, TOURNAMENTS)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)

    def test_StateQUITFromTOURNAMENTS_NO(self):
        self.test_StateQUITFromTOURNAMENTS_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_YES(self):
        self.test_StateQUITFromTOURNAMENTS_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)

    def test_StateTOURNAMENTSFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,TOURNAMENTS))

    # -----------------------------------------------------------------------------------------------------    

    def test_StateTOURNAMENTSFromQUITFromLOBBY(self):
        self.renderer.quit_state = LOBBY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOBBY)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (LOBBY,TOURNAMENTS))
        self.assertEquals(self.renderer.call_hideLobby, True)
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (SEATING,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (IDLE,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (REBUY,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (MUCK,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, True)

    def test_StateTOURNAMENTSFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (JOINING,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    def test_StateTOURNAMENTSFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(TOURNAMENTS)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,TOURNAMENTS))
        self.assertEquals(self.renderer.call_showTournaments, False)

    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromTOURNAMENTS_REGISTER_Without_INTERFACE(self):
        self.renderer.state = TOURNAMENTS_REGISTER
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_REGISTER_COMMON(self):
        self.renderer.state = TOURNAMENTS_REGISTER
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)

    def test_StateQUITFromTOURNAMENTS_REGISTER_NO(self):
        self.test_StateQUITFromTOURNAMENTS_REGISTER_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_REGISTER_YES(self):
        self.test_StateQUITFromTOURNAMENTS_REGISTER_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)

    def test_StateTOURNAMENTS_REGISTERFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,TOURNAMENTS_REGISTER))


    # -----------------------------------------------------------------------------------------------------    

    def test_StateTOURNAMENTS_REGISTERFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(TOURNAMENTS_REGISTER, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.call_hideTournaments, False)

    def test_StateTOURNAMENTS_REGISTERFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (SEATING,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (IDLE,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (REBUY,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (MUCK,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,TOURNAMENTS_REGISTER))


    def test_StateTOURNAMENTS_REGISTERFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (JOINING,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,TOURNAMENTS_REGISTER))

    def test_StateTOURNAMENTS_REGISTERFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(TOURNAMENTS_REGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_REGISTER))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,TOURNAMENTS_REGISTER))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromTOURNAMENTS_UNREGISTER_Without_INTERFACE(self):
        self.renderer.state = TOURNAMENTS_UNREGISTER
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_UNREGISTER_COMMON(self):
        self.renderer.state = TOURNAMENTS_UNREGISTER
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)

    def test_StateQUITFromTOURNAMENTS_UNREGISTER_NO(self):
        self.test_StateQUITFromTOURNAMENTS_UNREGISTER_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromTOURNAMENTS_UNREGISTER_YES(self):
        self.test_StateQUITFromTOURNAMENTS_UNREGISTER_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,TOURNAMENTS_UNREGISTER))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.call_hideTournaments, False)

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (SEATING,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (IDLE,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (REBUY,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (MUCK,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,TOURNAMENTS_UNREGISTER))


    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (JOINING,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,TOURNAMENTS_UNREGISTER))

    def test_StateTOURNAMENTS_UNREGISTERFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(TOURNAMENTS_UNREGISTER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,TOURNAMENTS_UNREGISTER))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,TOURNAMENTS_UNREGISTER))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromCASHIER_Without_INTERFACE(self):
        self.renderer.state = CASHIER
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, CASHIER)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromCASHIER_COMMON(self):
        self.renderer.state = CASHIER
	self.assertEquals(self.renderer.state, CASHIER)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)

    def test_StateQUITFromCASHIER_NO(self):
        self.test_StateQUITFromCASHIER_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, CASHIER)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromCASHIER_YES(self):
        self.test_StateQUITFromCASHIER_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, CASHIER)

    def test_StateCASHIERFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,CASHIER))


    # -----------------------------------------------------------------------------------------------------    

    def test_StateCASHIERFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,CASHIER))
        self.assertEquals(self.renderer.call_hideTournaments, True)
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (SEATING,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)
#        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (IDLE,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (REBUY,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (MUCK,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_PERSONAL_INFO, True)

    def test_StateCASHIERFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)


    def test_StateCASHIERFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (JOINING,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    def test_StateCASHIERFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(CASHIER)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CASHIER))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,CASHIER))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)

    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromLOGIN_Without_INTERFACE(self):
        self.renderer.state = LOGIN
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, LOGIN)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLOGIN_COMMON(self):
        self.renderer.state = LOGIN
	self.assertEquals(self.renderer.state, LOGIN)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)

    def test_StateQUITFromLOGIN_NO(self):
        self.test_StateQUITFromLOGIN_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, LOGIN)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLOGIN_YES(self):
        self.test_StateQUITFromLOGIN_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, LOGIN)

    def test_StateLOGINFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,LOGIN))


    # -----------------------------------------------------------------------------------------------------    

    def test_StateLOGINFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # because already logged
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,LOGIN))
        self.assertEquals(self.renderer.call_hideTournaments, False)

    def test_StateLOGINFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,LOGIN))

    def test_StateLOGINFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (SEATING,LOGIN))

    def test_StateLOGINFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # because already logged
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (IDLE,LOGIN))

    def test_StateLOGINFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,LOGIN))

    def test_StateLOGINFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,LOGIN))

    def test_StateLOGINFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,LOGIN))

    def test_StateLOGINFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,LOGIN))

    def test_StateLOGINFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (REBUY,LOGIN))

    def test_StateLOGINFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (MUCK,LOGIN))

    def test_StateLOGINFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,LOGIN))

    def test_StateLOGINFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,LOGIN))

    def test_StateLOGINFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,LOGIN))

    def test_StateLOGINFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,LOGIN))

    def test_StateLOGINFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,LOGIN))


    def test_StateLOGINFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (JOINING,LOGIN))

    def test_StateLOGINFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,LOGIN))

    def test_StateLOGINFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,LOGIN))

    def test_StateLOGINFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,LOGIN))

    def test_StateLOGINFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(LOGIN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LOGIN))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,LOGIN))

    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromSEATING_Without_INTERFACE(self):
        self.renderer.state = SEATING
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, SEATING)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSEATING_COMMON(self):
        self.renderer.state = SEATING
	self.assertEquals(self.renderer.state, SEATING)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)

    def test_StateQUITFromSEATING_NO(self):
        self.test_StateQUITFromSEATING_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, SEATING)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSEATING_YES(self):
        self.test_StateQUITFromSEATING_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, SEATING)

    def test_StateSEATINGFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(SEATING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (SEATING,SEATING))


    # -----------------------------------------------------------------------------------------------------    
    def test_StateSEATINGFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,SEATING))
        self.assertEquals(self.renderer.call_hideTournaments, True)

    def test_StateSEATINGFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,SEATING))

    def test_StateSEATINGFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (SEATING,SEATING))

    def test_StateSEATINGFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (IDLE,SEATING))

    def test_StateSEATINGFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,SEATING))

    def test_StateSEATINGFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,SEATING))

    def test_StateSEATINGFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,SEATING))

    def test_StateSEATINGFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,SEATING))

    def test_StateSEATINGFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (REBUY,SEATING))

    def test_StateSEATINGFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (MUCK,SEATING))

    def test_StateSEATINGFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,SEATING))

    def test_StateSEATINGFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,SEATING))

    def test_StateSEATINGFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,SEATING))

    def test_StateSEATINGFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,SEATING))

    def test_StateSEATINGFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,SEATING))


    def test_StateSEATINGFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (JOINING,SEATING))

    def test_StateSEATINGFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,SEATING))

    def test_StateSEATINGFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,SEATING))

    def test_StateSEATINGFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,SEATING))

    def test_StateSEATINGFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(SEATING, PacketPokerId())
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEATING))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,SEATING))

    # -----------------------------------------------------------------------------------------------------    

    def test_StateQUITFromBUY_IN_Without_INTERFACE(self):
        self.renderer.state = BUY_IN
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, BUY_IN)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromBUY_IN_COMMON(self):
        self.renderer.state = BUY_IN
	self.assertEquals(self.renderer.state, BUY_IN)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)

    def test_StateQUITFromBUY_IN_NO(self):
        self.test_StateQUITFromBUY_IN_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, BUY_IN)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromBUY_IN_YES(self):
        self.test_StateQUITFromBUY_IN_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)

    def test_StateBUY_INFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,BUY_IN))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateBUY_INFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,BUY_IN))
        self.assertEquals(self.renderer.call_hideTournaments, False)

    def test_StateBUY_INFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,BUY_IN))

    def test_StateBUY_INFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (SEATING,BUY_IN))

    def test_StateBUY_INFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (IDLE,BUY_IN))

    def test_StateBUY_INFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,BUY_IN))

    def test_StateBUY_INFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,BUY_IN))

    def test_StateBUY_INFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(BUY_IN, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_requestBuyIn, True)
        # we can have a idle state if the user has not enough money to go on a table
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,BUY_IN))

    def test_StateBUY_INFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (REBUY,BUY_IN))

    def test_StateBUY_INFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (MUCK,BUY_IN))

    def test_StateBUY_INFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,BUY_IN))

    def test_StateBUY_INFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,BUY_IN))

    def test_StateBUY_INFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,BUY_IN))

    def test_StateBUY_INFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,BUY_IN))

    def test_StateBUY_INFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,BUY_IN))


    def test_StateBUY_INFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (JOINING,BUY_IN))

    def test_StateBUY_INFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,BUY_IN))

    def test_StateBUY_INFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,BUY_IN))

    def test_StateBUY_INFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,BUY_IN))

    def test_StateBUY_INFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(BUY_IN)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,BUY_IN))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,BUY_IN))

# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromSEARCHING_MY_Without_INTERFACE(self):
        self.renderer.state = SEARCHING_MY
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, SEARCHING_MY)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSEARCHING_MY_COMMON(self):
        self.renderer.state = SEARCHING_MY
	self.assertEquals(self.renderer.state, SEARCHING_MY)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)

    def test_StateQUITFromSEARCHING_MY_NO(self):
        self.test_StateQUITFromSEARCHING_MY_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSEARCHING_MY_YES(self):
        self.test_StateQUITFromSEARCHING_MY_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)

    def test_StateSEARCHING_MYFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,SEARCHING_MY))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateSEARCHING_MYFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,SEARCHING_MY))
        self.assertEquals(self.renderer.call_hideTournaments, True)

    def test_StateSEARCHING_MYFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (SEATING,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (IDLE,SEARCHING_MY))

    def test_StateSEARCHING_MYFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,SEARCHING_MY))

    def test_StateSEARCHING_MYFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (REBUY,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (MUCK,SEARCHING_MY))

    def test_StateSEARCHING_MYFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,SEARCHING_MY))

    def test_StateSEARCHING_MYFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,SEARCHING_MY))
        


    def test_StateSEARCHING_MYFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (JOINING,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,SEARCHING_MY))
        

    def test_StateSEARCHING_MYFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(SEARCHING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SEARCHING_MY))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,SEARCHING_MY))
        

# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromHAND_LIST_Without_INTERFACE(self):
        self.renderer.state = HAND_LIST
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, HAND_LIST)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromHAND_LIST_COMMON(self):
        self.renderer.state = HAND_LIST
	self.assertEquals(self.renderer.state, HAND_LIST)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)

    def test_StateQUITFromHAND_LIST_NO(self):
        self.test_StateQUITFromHAND_LIST_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, HAND_LIST)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromHAND_LIST_YES(self):
        self.test_StateQUITFromHAND_LIST_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)

    def test_StateHAND_LISTFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,HAND_LIST))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateHAND_LISTFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,HAND_LIST))
        self.assertEquals(self.renderer.call_hideTournaments, True)
        self.assertEquals(self.renderer.call_queryHands, True)

    def test_StateHAND_LISTFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, True)

    def test_StateHAND_LISTFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (SEATING,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (IDLE,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, True)

    def test_StateHAND_LISTFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)


    def test_StateHAND_LISTFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (REBUY,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (MUCK,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, True)

    def test_StateHAND_LISTFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, True)

    def test_StateHAND_LISTFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (JOINING,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

    def test_StateHAND_LISTFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(HAND_LIST)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,HAND_LIST))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,HAND_LIST))
        self.assertEquals(self.renderer.call_queryHands, False)

# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromUSER_INFO_Without_INTERFACE(self):
        self.renderer.state = USER_INFO
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, USER_INFO)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromUSER_INFO_COMMON(self):
        self.renderer.state = USER_INFO
	self.assertEquals(self.renderer.state, USER_INFO)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)

    def test_StateQUITFromUSER_INFO_NO(self):
        self.test_StateQUITFromUSER_INFO_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, USER_INFO)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromUSER_INFO_YES(self):
        self.test_StateQUITFromUSER_INFO_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)

    def test_StateUSER_INFOFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet == None, True)
        
    # -----------------------------------------------------------------------------------------------------    
    def test_StateUSER_INFOFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,USER_INFO))
        self.assertEquals(self.renderer.call_hideTournaments, True)
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (SEATING,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (IDLE,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        


    def test_StateUSER_INFOFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (REBUY,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (MUCK,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        


    def test_StateUSER_INFOFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (JOINING,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

    def test_StateUSER_INFOFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(USER_INFO)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,USER_INFO))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,USER_INFO))
        self.assertEquals(self.renderer.protocol.send_packet != None, True)
        self.assertEquals(self.renderer.protocol.send_packet.type == PACKET_POKER_GET_USER_INFO, True)
        

# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromREBUY_Without_INTERFACE(self):
        self.renderer.state = REBUY
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, REBUY)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromREBUY_COMMON(self):
        self.renderer.state = REBUY
	self.assertEquals(self.renderer.state, REBUY)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)

    def test_StateQUITFromREBUY_NO(self):
        self.test_StateQUITFromREBUY_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, REBUY)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromREBUY_YES(self):
        self.test_StateQUITFromREBUY_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, REBUY)

    def test_StateREBUYFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (REBUY,REBUY))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateREBUYFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,REBUY))
        self.assertEquals(self.renderer.call_hideTournaments, False)


    def test_StateREBUYFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,REBUY))


    def test_StateREBUYFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (SEATING,REBUY))


    def test_StateREBUYFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (IDLE,REBUY))


    def test_StateREBUYFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,REBUY))


    def test_StateREBUYFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,REBUY))


    def test_StateREBUYFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(REBUY, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,REBUY))
        self.assertEquals(self.renderer.call_requestBuyIn, True)


    def test_StateREBUYFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,REBUY))


    def test_StateREBUYFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (MUCK,REBUY))


    def test_StateREBUYFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,REBUY))


    def test_StateREBUYFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,REBUY))


    def test_StateREBUYFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,REBUY))


    def test_StateREBUYFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,REBUY))


    def test_StateREBUYFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,REBUY))


    def test_StateREBUYFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (JOINING,REBUY))


    def test_StateREBUYFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,REBUY))


    def test_StateREBUYFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,REBUY))


    def test_StateREBUYFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,REBUY))


    def test_StateREBUYFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(REBUY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,REBUY))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,REBUY))

# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromMUCK_Without_INTERFACE(self):
        self.renderer.state = MUCK
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, MUCK)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromMUCK_COMMON(self):
        self.renderer.state = MUCK
	self.assertEquals(self.renderer.state, MUCK)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)

    def test_StateQUITFromMUCK_NO(self):
        self.test_StateQUITFromMUCK_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, MUCK)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromMUCK_YES(self):
        self.test_StateQUITFromMUCK_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, MUCK)

    def test_StateMUCKFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(MUCK)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (MUCK,MUCK))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateMUCKFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,MUCK))
        self.assertEquals(self.renderer.call_hideTournaments, False)
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (SEATING,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (IDLE,MUCK))
        self.assertEquals(self.renderer.call_showMuck, True)

    def test_StateMUCKFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (REBUY,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (JOINING,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)

    def test_StateMUCKFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(MUCK, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,MUCK))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,MUCK))
        self.assertEquals(self.renderer.call_showMuck, False)
# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromPAY_BLIND_ANTE_Without_INTERFACE(self):
        self.renderer.state = PAY_BLIND_ANTE
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromPAY_BLIND_ANTE_COMMON(self):
        self.renderer.state = PAY_BLIND_ANTE
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)

    def test_StateQUITFromPAY_BLIND_ANTE_NO(self):
        self.test_StateQUITFromPAY_BLIND_ANTE_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromPAY_BLIND_ANTE_YES(self):
        self.test_StateQUITFromPAY_BLIND_ANTE_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)

    def test_StatePAY_BLIND_ANTEFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,PAY_BLIND_ANTE))

    # -----------------------------------------------------------------------------------------------------    
    def test_StatePAY_BLIND_ANTEFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.call_hideTournaments, True)

    def test_StatePAY_BLIND_ANTEFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,PAY_BLIND_ANTE))

    def test_StatePAY_BLIND_ANTEFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (SEATING,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (IDLE,PAY_BLIND_ANTE))

    def test_StatePAY_BLIND_ANTEFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,PAY_BLIND_ANTE))

    def test_StatePAY_BLIND_ANTEFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (REBUY,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, True)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (MUCK,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,PAY_BLIND_ANTE))

    def test_StatePAY_BLIND_ANTEFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (JOINING,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,PAY_BLIND_ANTE))


    def test_StatePAY_BLIND_ANTEFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(PAY_BLIND_ANTE, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,PAY_BLIND_ANTE))


# -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromPAY_BLIND_ANTE_SEND_Without_INTERFACE(self):
        self.renderer.state = PAY_BLIND_ANTE_SEND
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromPAY_BLIND_ANTE_SEND_COMMON(self):
        self.renderer.state = PAY_BLIND_ANTE_SEND
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)

    def test_StateQUITFromPAY_BLIND_ANTE_SEND_NO(self):
        self.test_StateQUITFromPAY_BLIND_ANTE_SEND_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromPAY_BLIND_ANTE_SEND_YES(self):
        self.test_StateQUITFromPAY_BLIND_ANTE_SEND_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)

    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,PAY_BLIND_ANTE_SEND))

    # -----------------------------------------------------------------------------------------------------    
    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.call_hideTournaments, False)


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (SEATING,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (IDLE,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (REBUY,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (MUCK,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (JOINING,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,PAY_BLIND_ANTE_SEND))


    def test_StatePAY_BLIND_ANTE_SENDFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(PAY_BLIND_ANTE_SEND, "dummy", 1)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,PAY_BLIND_ANTE_SEND))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,PAY_BLIND_ANTE_SEND))


    # -----------------------------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromJOINING_Without_INTERFACE(self):
        self.renderer.state = JOINING
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, JOINING)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromJOINING_COMMON(self):
        self.renderer.state = JOINING
	self.assertEquals(self.renderer.state, JOINING)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)

    def test_StateQUITFromJOINING_NO(self):
        self.test_StateQUITFromJOINING_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, JOINING)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromJOINING_YES(self):
        self.test_StateQUITFromJOINING_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, JOINING)

    def test_StateJOININGFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (JOINING,JOINING))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateJOININGFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,JOINING))
        self.assertEquals(self.renderer.call_hideTournaments, False)


    def test_StateJOININGFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,JOINING))


    def test_StateJOININGFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (SEATING,JOINING))


    def test_StateJOININGFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (IDLE,JOINING))


    def test_StateJOININGFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,JOINING))


    def test_StateJOININGFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,JOINING))


    def test_StateJOININGFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,JOINING))


    def test_StateJOININGFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,JOINING))


    def test_StateJOININGFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (REBUY,JOINING))


    def test_StateJOININGFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (MUCK,JOINING))


    def test_StateJOININGFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,JOINING))


    def test_StateJOININGFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,JOINING))


    def test_StateJOININGFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,JOINING))


    def test_StateJOININGFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,JOINING))


    def test_StateJOININGFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,JOINING))


    def test_StateJOININGFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,JOINING))


    def test_StateJOININGFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,JOINING))


    def test_StateJOININGFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,JOINING))


    def test_StateJOININGFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(JOINING)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,JOINING))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromJOINING_MY_Without_INTERFACE(self):
        self.renderer.state = JOINING_MY
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, JOINING_MY)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromJOINING_MY_COMMON(self):
        self.renderer.state = JOINING_MY
	self.assertEquals(self.renderer.state, JOINING_MY)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)

    def test_StateQUITFromJOINING_MY_NO(self):
        self.test_StateQUITFromJOINING_MY_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, JOINING_MY)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromJOINING_MY_YES(self):
        self.test_StateQUITFromJOINING_MY_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)

    def test_StateJOINING_MYFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,JOINING_MY))

    # -----------------------------------------------------------------------------------------------------    
    def test_StateJOINING_MYFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,JOINING_MY))
        self.assertEquals(self.renderer.call_hideTournaments, False)


    def test_StateJOINING_MYFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (SEATING,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (IDLE,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
        self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (REBUY,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (MUCK,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (JOINING,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,JOINING_MY))


    def test_StateJOINING_MYFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(JOINING_MY)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,JOINING_MY))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,JOINING_MY))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromLEAVING_Without_INTERFACE(self):
        self.renderer.state = LEAVING
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, LEAVING)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLEAVING_COMMON(self):
        self.renderer.state = LEAVING
	self.assertEquals(self.renderer.state, LEAVING)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)

    def test_StateQUITFromLEAVING_NO(self):
        self.test_StateQUITFromLEAVING_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, LEAVING)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLEAVING_YES(self):
        self.test_StateQUITFromLEAVING_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, LEAVING)

    def test_StateLEAVINGFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,LEAVING))


    # -----------------------------------------------------------------------------------------------------    
    def test_StateLEAVINGFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (SEATING,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (IDLE,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        ############ FIX ME ############ hideHands should be True else we have a windows in the nature
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (REBUY,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (MUCK,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (JOINING,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))


    def test_StateLEAVINGFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(LEAVING, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 4)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,LEAVING))
        self.assertEquals(self.renderer.change_state[2], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[3], (IDLE,LOBBY))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromLEAVING_CONFIRM_Without_INTERFACE(self):
        self.renderer.state = LEAVING_CONFIRM
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLEAVING_CONFIRM_COMMON(self):
        self.renderer.state = LEAVING_CONFIRM
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)

    def test_StateQUITFromLEAVING_CONFIRM_NO(self):
        self.test_StateQUITFromLEAVING_CONFIRM_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromLEAVING_CONFIRM_YES(self):
        self.test_StateQUITFromLEAVING_CONFIRM_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)

    def test_StateLEAVING_CONFIRMFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(LEAVING_CONFIRM)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,LEAVING_CONFIRM))

    def test_StateLEAVING_CONFIRMFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (TOURNAMENTS,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (SEARCHING_MY,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (SEATING,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (SEATING,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (IDLE,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (IDLE,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (LOGIN,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (HAND_LIST,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (USER_INFO,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (BUY_IN,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (REBUY,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (REBUY,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (MUCK,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (MUCK,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (PAY_BLIND_ANTE,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (PAY_BLIND_ANTE_SEND,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (CASHIER,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (TOURNAMENTS_REGISTER,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (TOURNAMENTS_UNREGISTER,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (JOINING,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (JOINING,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (JOINING_MY,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))


    def test_StateLEAVING_CONFIRMFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 3)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,LEAVING_CONFIRM))



    def test_StateLEAVING_CONFIRMFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(LEAVING_CONFIRM, None, 0)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOBBY)
        self.assertEquals(len(self.renderer.change_state), 5)
        self.assertEquals(self.renderer.change_state[0], (QUIT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,LEAVING_CONFIRM))
        self.assertEquals(self.renderer.change_state[2], (SIT_OUT,LEAVING))
        self.assertEquals(self.renderer.change_state[3], (LEAVING,LEAVING_DONE))
        self.assertEquals(self.renderer.change_state[4], (IDLE,LOBBY))

    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromCANCELED_Without_INTERFACE(self):
        self.renderer.state = CANCELED
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, CANCELED)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromCANCELED_COMMON(self):
        self.renderer.state = CANCELED
	self.assertEquals(self.renderer.state, CANCELED)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CANCELED)

    def test_StateQUITFromCANCELED_NO(self):
        self.test_StateQUITFromCANCELED_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, CANCELED)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromCANCELED_YES(self):
        self.test_StateQUITFromCANCELED_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, CANCELED)

    def test_StateCANCELEDFromQUITFromCANCELED(self):
        self.renderer.quit_state = CANCELED
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CANCELED)
        self.renderer.changeState(CANCELED)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CANCELED)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,CANCELED))
        self.assertEquals(self.renderer.change_state[1], (CANCELED,CANCELED))


    # -----------------------------------------------------------------------------------------------------

    def test_StateQUITFromSIT_OUT_Without_INTERFACE(self):
        self.renderer.state = SIT_OUT
        self.renderer.factory.interface = None
	self.assertEquals(self.renderer.state, SIT_OUT)
	self.assertEquals(self.renderer.factory.interface, None)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        # none because there is no confirmation without interface
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSIT_OUT_COMMON(self):
        self.renderer.state = SIT_OUT
	self.assertEquals(self.renderer.state, SIT_OUT)
	self.assertEquals(self.renderer.call_showYesNo, False)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), False)
	self.assertEquals(self.renderer.quit_state, None)
        self.renderer.pythonEvent("QUIT")
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)

    def test_StateQUITFromSIT_OUT_NO(self):
        self.test_StateQUITFromSIT_OUT_COMMON()
        self.renderer.confirmQuit(response = False)
	self.assertEquals(self.renderer.state, SIT_OUT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.quit_state, None)

    def test_StateQUITFromSIT_OUT_YES(self):
        self.test_StateQUITFromSIT_OUT_COMMON()
        self.renderer.confirmQuit(response = True)
	self.assertEquals(self.renderer.state, QUIT_DONE)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.send_packet.type, PACKET_QUIT)
	self.assertEquals(self.renderer.interactors.call_destroy, True)
	self.assertEquals(self.renderer.factory.call_quit, True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)

    def test_StateSIT_OUTFromQUITFromSIT_OUT(self):
        self.renderer.quit_state = SIT_OUT
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SIT_OUT)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SIT_OUT)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (SIT_OUT,SIT_OUT))
    # -----------------------------------------------------------------------------------------------------

    def test_StateSIT_OUTFromQUITFromTOURNAMENTS(self):
        self.renderer.quit_state = TOURNAMENTS
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS,SIT_OUT))
        self.assertEquals(self.renderer.call_hideTournaments, False)


    def test_StateSIT_OUTFromQUITFromSEARCHING_MY(self):
        self.renderer.quit_state = SEARCHING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEARCHING_MY)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEARCHING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (SEARCHING_MY,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromSEATING(self):
        self.renderer.quit_state = SEATING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, SEATING)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, SEATING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (SEATING,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromIDLE(self):
        self.renderer.quit_state = IDLE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, IDLE)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (IDLE,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromLOGIN(self):
        self.renderer.quit_state = LOGIN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LOGIN)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LOGIN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (LOGIN,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromHAND_LIST(self):
        self.renderer.quit_state = HAND_LIST
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, HAND_LIST)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.call_hideHands, False)
	self.assertEquals(self.renderer.state, HAND_LIST)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (HAND_LIST,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromUSER_INFO(self):
        self.renderer.quit_state = USER_INFO
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, USER_INFO)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, USER_INFO)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (USER_INFO,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromBUY_IN(self):
        self.renderer.quit_state = BUY_IN
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, BUY_IN)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, BUY_IN)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (BUY_IN,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromREBUY(self):
        self.renderer.quit_state = REBUY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, REBUY)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
        self.assertEquals(self.renderer.state, REBUY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (REBUY,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromMUCK(self):
        self.renderer.quit_state = MUCK
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, MUCK)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, MUCK)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.call_hideMuck, False)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (MUCK,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromPAY_BLIND_ANTE(self):
        self.renderer.quit_state = PAY_BLIND_ANTE
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, IDLE)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromPAY_BLIND_ANTE_SEND(self):
        self.renderer.quit_state = PAY_BLIND_ANTE_SEND
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, PAY_BLIND_ANTE_SEND)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, PAY_BLIND_ANTE_SEND)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (PAY_BLIND_ANTE_SEND,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromCASHIER(self):
        self.renderer.quit_state = CASHIER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, CASHIER)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, CASHIER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (CASHIER,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromTOURNAMENTS_REGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_REGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_REGISTER)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_REGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_REGISTER,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromTOURNAMENTS_UNREGISTER(self):
        self.renderer.quit_state = TOURNAMENTS_UNREGISTER
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, TOURNAMENTS_UNREGISTER)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, TOURNAMENTS_UNREGISTER)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (TOURNAMENTS_UNREGISTER,SIT_OUT))



    def test_StateSIT_OUTFromQUITFromJOINING(self):
        self.renderer.quit_state = JOINING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (JOINING,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromJOINING_MY(self):
        self.renderer.quit_state = JOINING_MY
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, JOINING_MY)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, JOINING_MY)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (JOINING_MY,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromLEAVING(self):
        self.renderer.quit_state = LEAVING
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (LEAVING,SIT_OUT))


    def test_StateSIT_OUTFromQUITFromLEAVING_CONFIRM(self):
        self.renderer.quit_state = LEAVING_CONFIRM
        self.renderer.state = QUIT
        self.renderer.call_showYesNo = True
        self.renderer.factory.interface.callbacks[INTERFACE_YESNO] = True
	self.assertEquals(self.renderer.state, QUIT)
	self.assertEquals(self.renderer.call_showYesNo, True)
	self.assertEquals(self.renderer.call_hideYesNo, False)
	self.assertEquals(self.renderer.send_packet, None)
	self.assertEquals(self.renderer.interactors.call_destroy, False)
	self.assertEquals(self.renderer.factory.call_quit, False)
	self.assertEquals(self.renderer.factory.interface.callbacks.has_key(INTERFACE_YESNO), True)
	self.assertEquals(self.renderer.quit_state, LEAVING_CONFIRM)
        self.renderer.changeState(SIT_OUT)
	self.assertEquals(self.renderer.call_hideYesNo, True)
	self.assertEquals(self.renderer.state, LEAVING_CONFIRM)
        self.assertEquals(len(self.renderer.change_state), 2)
        self.assertEquals(self.renderer.change_state[0], (QUIT,SIT_OUT))
        self.assertEquals(self.renderer.change_state[1], (LEAVING_CONFIRM,SIT_OUT))


# -----------------------------------------------------------------------------------------------------


def GetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PokerRendererTestCase))
    return suite
    
# -----------------------------------------------------------------------------------------------------
def GetTestedModule():
    return pokerrenderer
  
# -----------------------------------------------------------------------------------------------------
def Run(verbose = 2):
    return unittest.TextTestRunner(verbosity=verbose).run(GetTestSuite())
    
# -----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if Run().wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

# Interpreted by emacs
# Local Variables:
# compile-command: "( cd .. ; ./config.status tests/test-quit.py ) ; ( cd ../tests ; make TESTS='test-quit.py' check )"
# End:
