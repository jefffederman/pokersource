#
# -*- coding: iso-8859-1 -*-
#
# Copyright (C) 2006, 2007 Loic Dachary <loic@dachary.org>
# Copyright (C) 2004, 2005, 2006 Mekensleep
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
#  Henry Precheur <henry@precheur.org> (2004)
#

from twisted.internet import reactor

from re import match
from types import *
from string import split, join
import time

from pokerengine.pokergame import PokerGameServer, history2messages
from pokerengine.pokercards import PokerCards

from pokernetwork.pokerpackets import *
from pokernetwork import pokeravatar

class PokerPredefinedDecks:
    def __init__(self, decks):
        self.decks = decks
        self.index = 0
        
    def shuffle(self, deck):
        deck[:] = self.decks[self.index][:]
        self.index += 1
        if self.index >= len(self.decks):
            self.index = 0
        
class PokerTable:

    def __init__(self, factory, id = 0, description = None):
        self.factory = factory
        settings = self.factory.settings
        self.game = PokerGameServer("poker.%s.xml", factory.dirs)
        self.game.verbose = factory.verbose
        self.history_index = 0
        predefined_decks = settings.headerGetList("/server/decks/deck")
        if predefined_decks:
            self.game.shuffler = PokerPredefinedDecks(map(lambda deck: self.game.eval.string2card(split(deck)), predefined_decks))
        self.observers = []
        self.waiting = []
        game = self.game
        game.id = id
        game.name = description["name"]
        game.setVariant(description["variant"])
        game.setBettingStructure(description["betting_structure"])
        game.setMaxPlayers(int(description["seats"]))
        self.skin = description.get("skin", "default")
        self.currency_serial = int(description.get("currency_serial", 0))
        self.playerTimeout = int(description.get("player_timeout", 60))
        self.muckTimeout = int(description.get("muck_timeout", 5))
        self.transient = description.has_key("transient")
        self.tourney = description.get("tourney", None)
        self.delays = settings.headerGetProperties("/server/delays")[0]
        self.autodeal = settings.headerGet("/server/@autodeal") == "yes"
        self.temporaryPlayersPattern = settings.headerGet("/server/users/@temporary")
        self.cache = self.createCache()
        self.owner = 0
        self.serial2client = {}
        self.timer_info = {
            "playerTimeout": None,
            "playerTimeoutSerial": 0,
            "muckTimeout": None,
            }
        self.timeout_policy = "sitOut"
        self.previous_dealer = -1
        self.game_delay = {
            "start": 0,
            "delay": 0,
            }            

    def isValid(self):
        return hasattr(self, "factory")

    def destroy(self):
        if self.transient:
            self.factory.destroyTable(self.game.id)
            
        self.broadcast(PacketPokerTableDestroy(game_id = self.game.id))
        for client in self.serial2client.values() + self.observers:
            del client.tables[self.game.id]
            
        self.factory.deleteTable(self)
        del self.factory

    def getName(self, serial):
        if self.serial2client.has_key(serial):
            name = self.serial2client[serial].getName()
        else:
            name = self.factory.getName(serial)
        return name

    def getPlayerInfo(self, serial):
        if self.serial2client.has_key(serial):
            info = self.serial2client[serial].getPlayerInfo()
        else:
            info = self.factory.getPlayerInfo(serial)
        return info
        
    def listPlayers(self):
        players = []
        game = self.game
        for serial in game.serialsAll():
            players.append((self.getName(serial), game.getPlayerMoney(serial), 0))
        return players
        
    def createCache(self):
        return { "board": PokerCards(), "pockets": {} }
    
    def cancelDealTimeout(self):
        info = self.timer_info
        if info.has_key("dealTimeout"):
            if info["dealTimeout"].active():
                info["dealTimeout"].cancel()
            del info["dealTimeout"]

    def beginTurn(self):
        self.cancelDealTimeout()
        if not self.isRunning():
            self.historyReset()
            hand_serial = self.factory.getHandSerial()
            game = self.game
            print "Dealing hand %s/%d" % ( game.name, hand_serial )
            game.setTime(time.time())
            game.beginTurn(hand_serial)
            for player in game.playersAll():
                player.getUserData()['ready'] = True
        
    def historyReset(self):
        self.history_index = 0
        self.cache = self.createCache()

    def toPacket(self):
        game = self.game
        return PacketPokerTable(id = game.id,
                                name = game.name,
                                variant = game.variant,
                                betting_structure = game.betting_structure,
                                seats = game.max_players,
                                players = game.allCount(),
                                hands_per_hour = game.stats["hands_per_hour"],
                                average_pot = game.stats["average_pot"],
                                percent_flop = game.stats["percent_flop"],
                                player_timeout = self.playerTimeout,
                                muck_timeout = self.muckTimeout,
                                observers = len(self.observers),
                                waiting = len(self.waiting),
                                skin = self.skin,
                                currency_serial = self.currency_serial)
                
    def cards2packets(self, game_id, board, pockets, cache):
        packets = []
        #
        # If no pockets or board specified (different from empty pockets),
        # ignore and keep the cached values
        #
        if board != None:
            if board != cache["board"]:
                packets.append(PacketPokerBoardCards(game_id = game_id,
                                                     cards = board.tolist(False)))
                cache["board"] = board.copy()

        if pockets != None:
            #
            # Send new pockets or pockets that changed
            #
            for (serial, pocket) in pockets.iteritems():
                if not cache["pockets"].has_key(serial) or cache["pockets"][serial] != pocket:
                    packets.append(PacketPokerPlayerCards(game_id = game_id,
                                                          serial = serial,
                                                          cards = pocket.toRawList()))
                if not cache["pockets"].has_key(serial):
                    cache["pockets"][serial] = pocket.copy()
        return packets

    def broadcast(self, packets):
        game = self.game

        if not type(packets) is ListType:
            packets = ( packets, )
            
        for packet in packets:
            keys = game.serial2player.keys()
            if self.factory.verbose > 1:
                print "broadcast%s %s " % ( keys, packet )
            for serial in keys:
                #
                # Player may be in game but disconnected.
                #
                if self.serial2client.has_key(serial):
                    client = self.serial2client[serial]
                    client.sendPacket(self.private2public(packet, serial))
            for client in self.observers:
                client.sendPacket(self.private2public(packet, 0))

    def private2public(self, packet, serial):
        game = self.game
        #
        # Cards private to each player are shown only to the player
        #
        if packet.type == PACKET_POKER_PLAYER_CARDS and packet.serial != serial:
            private = PacketPokerPlayerCards(game_id = packet.game_id,
                                             serial = packet.serial,
                                             cards = PokerCards(packet.cards).tolist(False))
            return private
        else:
            return packet
        
    def history2packets(self, history, game_id, cache):
        game_index = 0
        player_list_index = 7
        packets = []
        for event in history:
            type = event[0]
            if type == "game":
                (type, level, hand_serial, hands_count, time, variant, betting_structure, player_list, dealer, serial2chips) = event
                if len(serial2chips) > 1:
                    nochips = 0
                    for (serial, chips) in serial2chips.iteritems():
                        if serial == 'values':
                            continue
                        packets.append(PacketPokerPlayerChips(game_id = game_id,
                                                              serial = serial,
                                                              bet = nochips,
                                                              money = chips))
                packets.append(PacketPokerInGame(game_id = game_id,
                                                 players = player_list))
                #
                # This may happen, for instance, if a turn is canceled
                #
                if self.previous_dealer == dealer:
                    previous_dealer = -1
                else:
                    previous_dealer = self.previous_dealer
                packets.append(PacketPokerDealer(game_id = game_id,
                                                 dealer = dealer,
                                                 previous_dealer = previous_dealer))
                self.previous_dealer = dealer
                packets.append(PacketPokerStart(game_id = game_id,
                                                hand_serial = hand_serial,
                                                hands_count = hands_count,
                                                time = time,
                                                level = level))
                
            elif type == "wait_for":
                (type, serial, reason) = event
                packets.append(PacketPokerWaitFor(game_id = game_id,
                                                  serial = serial,
                                                  reason = reason))
                
            elif type == "player_list":
                (type, player_list) = event
                packets.append(PacketPokerInGame(game_id = game_id,
                                                 players = player_list))

            elif type == "round":
                (type, name, board, pockets) = event
                packets.extend(self.cards2packets(game_id, board, pockets, cache))
                packets.append(PacketPokerState(game_id = game_id,
                                                string = name))

            elif type == "position":
                (type, position) = event
                packets.append(PacketPokerPosition(game_id = game_id,
                                                   position = position))
                
            elif type == "showdown":
                (type, board, pockets) = event
                packets.extend(self.cards2packets(game_id, board, pockets, cache))
                
            elif type == "blind_request":
                (type, serial, amount, dead, state) = event
                packets.append(PacketPokerBlindRequest(game_id = game_id,
                                                       serial = serial,
                                                       amount = amount,
                                                       dead = dead,
                                                       state = state))

            elif type == "wait_blind":
                (type, serial) = event
                pass
                    
            elif type == "blind":
                (type, serial, amount, dead) = event
                packets.append(PacketPokerBlind(game_id = game_id,
                                                serial = serial,
                                                amount = amount,
                                                dead = dead))

            elif type == "ante_request":
                (type, serial, amount) = event
                packets.append(PacketPokerAnteRequest(game_id = game_id,
                                                      serial = serial,
                                                      amount = amount))

            elif type == "ante":
                (type, serial, amount) = event
                packets.append(PacketPokerAnte(game_id = game_id,
                                               serial = serial,
                                               amount = amount))

            elif type == "all-in":
                pass
            
            elif type == "call":
                (type, serial, amount) = event
                packets.append(PacketPokerCall(game_id = game_id,
                                               serial = serial))
                
            elif type == "check":
                (type, serial) = event
                packets.append(PacketPokerCheck(game_id = game_id,
                                                serial = serial))
                
            elif type == "fold":
                (type, serial) = event
                packets.append(PacketPokerFold(game_id = game_id,
                                               serial = serial))

            elif type == "raise":
                (type, serial, amount) = event
                packets.append(PacketPokerRaise(game_id = game_id,
                                                serial = serial,
                                                amount = amount))

            elif type == "canceled":
                (type, serial, amount) = event
                packets.append(PacketPokerCanceled(game_id = game_id,
                                                   serial = serial,
                                                   amount = amount))
                
            elif type == "muck":
                (type, muckable_serials) = event
                packets.append(PacketPokerMuckRequest(game_id = game_id,
                                                      muckable_serials = muckable_serials))
            
            elif type == "rake":
                (type, amount, serial2rake) = event
                packets.append(PacketPokerRake(game_id = game_id,
                                               value = amount))
                
            elif type == "end":
                (type, winners, showdown_stack) = event
                packets.append(PacketPokerState(game_id = game_id,
                                                string = "end"))
                packets.append(PacketPokerWin(game_id = game_id,
                                              serials = winners))

            elif type == "sitOut":
                (type, serial) = event
                packets.append(PacketPokerSitOut(game_id = game_id,
                                                 serial = serial))
                    
            elif type == "rebuy":
                (type, serial, amount) = event
                packets.append(PacketPokerRebuy(game_id = game_id,
                                                serial = serial,
                                                amount = amount))
                    
            elif type == "leave":
                (type, quitters) = event
                for (serial, seat) in quitters:
                    packets.append(PacketPokerPlayerLeave(game_id = game_id,
                                                          serial = serial,
                                                          seat = seat))
                
            elif type == "finish":
                pass
            
            else:
                print "history2packets: *ERROR* unknown history type %s " % type
        return packets

    def syncDatabase(self):
        game = self.game
        updates = {}
        serial2rake = {}
        reset_bet = False
        for event in game.historyGet()[self.history_index:]:
            type = event[0]
            if type == "game":
                pass
            
            elif type == "wait_for":
                pass
            
            elif type == "rebuy":
                pass
            
            elif type == "player_list":
                pass
            
            elif type == "round":
                pass
            
            elif type == "showdown":
                pass
                
            elif type == "rake":
                (type, amount, serial2rake) = event
                
            elif type == "muck":
                pass
                
            elif type == "position":
                pass
                
            elif type == "blind_request":
                pass
            
            elif type == "wait_blind":
                pass
            
            elif type == "blind":
                (type, serial, amount, dead) = event
                if not updates.has_key(serial):
                    updates[serial] = 0
                updates[serial] -= amount + dead

            elif type == "ante_request":
                pass
            
            elif type == "ante":
                (type, serial, amount) = event
                if not updates.has_key(serial):
                    updates[serial] = 0
                updates[serial] -= amount

            elif type == "all-in":
                pass
            
            elif type == "call":
                (type, serial, amount) = event
                if not updates.has_key(serial):
                    updates[serial] = 0
                updates[serial] -= amount
                
            elif type == "check":
                pass
                
            elif type == "fold":
                pass
            
            elif type == "raise":
                (type, serial, amount) = event
                if not updates.has_key(serial):
                    updates[serial] = 0
                updates[serial] -= amount

            elif type == "canceled":
                (type, serial, amount) = event
                if serial > 0 and amount > 0:
                    if not updates.has_key(serial):
                        updates[serial] = 0
                    updates[serial] += amount
                
            elif type == "end":
                (type, winners, showdown_stack) = event
                game_state = showdown_stack[0]
                for (serial, share) in game_state['serial2share'].iteritems():
                    if not updates.has_key(serial):
                        updates[serial] = 0
                    updates[serial] += share
                reset_bet = True

            elif type == "sitOut":
                pass

            elif type == "leave":
                pass
            
            elif type == "finish":
                (type, hand_serial) = event
                self.factory.saveHand(self.compressedHistory(game.historyGet()), hand_serial)
            
            else:
                print "syncDatabase: *ERROR* unknown history type %s " % type

        for (serial, amount) in updates.iteritems():
            self.factory.updatePlayerMoney(serial, game.id, amount)

        for (serial, rake) in serial2rake.iteritems():
            self.factory.updatePlayerRake(self.currency_serial, serial, rake)

        if reset_bet:
            self.factory.resetBet(game.id)
        elif hasattr(self, "factory") and self.factory.verbose > 2:
            (money, bet) = self.factory.tableMoneyAndBet(game.id)
            if bet and game.potAndBetsAmount() != bet:
                print " *ERROR* table %d bet mismatch %d in memory versus %d in database" % ( game.id, game.potAndBetsAmount(), bet)

    def historyReduce(self):
        game = self.game
        if self.history_index < len(game.historyGet()):
            game.historyReduce()
            self.history_index = len(game.historyGet())
            
    def compressedHistory(self, history):
        new_history = []
        cached_pockets = None
        cached_board = None
        for event in history:
            type = event[0]
            if ( type == "all-in" or
                 type == "wait_for" ) :
                pass
            
            elif type == "game":
                new_history.append(event)
                
            elif type == "round":
                (type, name, board, pockets) = event

                if pockets != cached_pockets:
                    cached_pockets = pockets
                else:
                    pockets = None

                if board != cached_board:
                    cached_board = board
                else:
                    board = None

                new_history.append((type, name, board, pockets))

            elif type == "showdown":
                (type, board, pockets) = event
                if pockets != cached_pockets:
                    cached_pockets = pockets
                else:
                    pockets = None

                if board != cached_board:
                    cached_board = board
                else:
                    board = None

                new_history.append((type, board, pockets))
            
            elif ( type == "call" or
                   type == "check" or
                   type == "fold" or
                   type == "raise" or
                   type == "canceled" or
                   type == "position" or
                   type == "blind" or
                   type == "ante" or
                   type == "player_list" ):
                new_history.append(event)

            elif type == "rake":
                new_history.append(event)
                
            elif type == "end":
                (type, winners, showdown_stack) = event
                new_history.append(event)

            elif type == "sitOut":
                new_history.append(event)
            
            elif type == "muck":
                pass
                    
            elif type == "leave":
                pass
                
            elif type == "finish":
                pass
            
            elif type == "rebuy":
                pass
            
            else:
                print "compressedHistory: *ERROR* unknown history type %s " % type

        return new_history

    def syncChat(self):
        (subject, messages) = history2messages(self.game, self.game.historyGet()[self.history_index:], serial2name = self.getName)
        if messages or subject:
            if self.factory.chat:
                if messages:
                    message = "".join(map(lambda line: "Dealer: " + line + "\n", messages))
                    self.broadcast(PacketPokerChat(game_id = self.game.id,
                                                   serial = 0,
                                                   message = message))

    def delayedActions(self):
        game = self.game
        for event in game.historyGet()[self.history_index:]:
            type = event[0]
            if type == "game":
                self.game_delay = {
                    "start": time.time(),
                    "delay": float(self.delays["autodeal"])
                    }
            elif ( type == "round" or
                   type == "position" or
                   type == "showdown" or
                   type == "finish" ):
                self.game_delay["delay"] += float(self.delays[type])
                if self.factory.verbose > 2:
                    print "delayedActions: game estimated duration is now " + str(self.game_delay["delay"]) + " and is running since %.02f " % (time.time() - self.game_delay["start"] ) + " seconds"

            elif type == "leave":
                (type, quitters) = event
                for (serial, seat) in quitters:
                    self.factory.leavePlayer(serial, game.id, self.currency_serial)
                    if self.serial2client.has_key(serial):
                        self.seated2observer(self.serial2client[serial])

    def tourneyEndTurn(self):
        if not self.tourney:
            return
        game = self.game
        for event in game.historyGet()[self.history_index:]:
            type = event[0]
            if type == "end":
                self.factory.tourneyEndTurn(self.tourney, game.id)
        
    def autoDeal(self):
        self.cancelDealTimeout()
        if not self.allReadyToPlay():
            #
            # All clients that fail to send a PokerReadyToPlay packet
            # within imposed delays after sending a PokerProcessingHand
            # are marked as bugous and their next PokerProcessingHand
            # request will be ignored.
            #
            for player in self.game.playersAll():
                if player.getUserData()['ready'] == False:
                    if self.serial2client.has_key(player.serial):
                        client = self.serial2client[player.serial]
                        if self.factory.verbose > 1: print "Player %d marked as having a bugous PokerProcessingHand protocol" % player.serial
                        client.bugous_processing_hand = True
            
        self.beginTurn()
        self.update()
        
    def autoDealCheck(self, autodeal_check, delta):
        if self.factory.verbose > 2:
            print "autoDealCheck"
        self.cancelDealTimeout()
        if autodeal_check > delta:
            if self.factory.verbose > 2:
                print "Autodeal scheduled in %f seconds" % delta
            self.timer_info["dealTimeout"] = reactor.callLater(delta, self.autoDeal)
            return
        game = self.game
        #
        # Issue a poker message to all players that are ready
        # to play.
        #
        serials = []
        for player in game.playersAll():
            if ( player.getUserData()['ready'] == True and
                 self.serial2client.has_key(player.serial) ):
                serials.append(player.serial)
        if serials:
            packet = PacketPokerMessage(game_id = self.game.id,
                                        string = "Waiting for players.\nNext hand will be dealt shortly.\n(maximum %d seconds)" % int(delta))
            for serial in serials:
                client = self.serial2client[serial]
                client.sendPacket(packet)
        if self.factory.verbose > 2:
            print "AutodealCheck(2) scheduled in %f seconds" % delta
        self.timer_info["dealTimeout"] = reactor.callLater(autodeal_check, self.autoDealCheck, autodeal_check, delta - autodeal_check)

    def scheduleAutoDeal(self):
        self.cancelDealTimeout()
        if self.factory.shutting_down:
            if self.factory.verbose > 2:
                print "Not autodealing because server is shutting down"
            return
        if not self.autodeal:
            if self.factory.verbose > 3:
                print "No autodeal"
            return
        if self.isRunning():
            if self.factory.verbose > 3:
                print "Not autodealing %d because game is running" % self.game.id
            return
        game = self.game
        if game.sitCount() < 2:
            if self.factory.verbose > 2:
                print "Not autodealing %d because less than 2 players willing to play" % self.game.id
            return
        if not game.isTournament():
            #
            # Do not auto deal a table where there are only temporary
            # users (i.e. bots)
            #
            onlyTemporaryPlayers = True
            for serial in game.serialsSit():
                if not match("^" + self.temporaryPlayersPattern, self.getName(serial)):
                    onlyTemporaryPlayers = False
                    break
            if onlyTemporaryPlayers:
                if self.factory.verbose > 2:
                    print "Not autodealing because player names sit in match %s" % self.temporaryPlayersPattern
                return

        delay = self.game_delay["delay"]
        if not self.allReadyToPlay() and delay > 0:
            delta = ( self.game_delay["start"] + delay ) - time.time()
            if delta < 0: delta = 0
            autodeal_max = float(self.delays.get("autodeal_max", 120))
            if delta > autodeal_max: delta = autodeal_max
        else:
            delta = 0
        if self.factory.verbose > 2:
            print "AutodealCheck scheduled in %f seconds" % delta
        autodeal_check = max(0.01, float(self.delays.get("autodeal_check", 15)))
        self.timer_info["dealTimeout"] = reactor.callLater(min(autodeal_check, delta), self.autoDealCheck, autodeal_check, delta)

    def updatePlayerUserData(self, serial, key, value):
        game = self.game
        player = game.getPlayer(serial)
        if player:
            user_data = player.getUserData()
            if user_data[key] != value:
                user_data[key] = value
                self.update()
        return True

    def allReadyToPlay(self):
        game = self.game
        status = True
        notready = []
        for player in game.playersAll():
            if player.getUserData()['ready'] == False:
                notready.append(str(player.serial))
                status = False
        if notready and self.factory.verbose > 3: print "allReadyToPlay: waiting for " + join(notready, ",")
        return status
        
    def readyToPlay(self, serial):
        self.updatePlayerUserData(serial, 'ready', True)
        return PacketAck()

    def processingHand(self, serial):
        self.updatePlayerUserData(serial, 'ready', False)
        return PacketAck()
        
    def update(self):
        if not self.isValid():
            return

        game = self.game
        history_tail = game.historyGet()[self.history_index:]
        
        self.updateTimers(history_tail)        
        packets = self.history2packets(history_tail, game.id, self.cache);
        self.syncDatabase()
        self.syncChat()
        self.delayedActions()
        if len(packets) > 0:
            self.broadcast(packets)
        self.tourneyEndTurn()
        if self.isValid():
            self.historyReduce()
            self.scheduleAutoDeal()

    def handReplay(self, client, hand):
        history = self.factory.loadHand(hand)
        if not history:
            return
        #print "handReplay"
        (type, level, hand_serial, hands_count, time, variant, betting_structure, player_list, dealer, serial2chips) = history[0]
        game = self.game
        for player in game.playersAll():
            client.sendPacketVerbose(PacketPokerPlayerLeave(game_id = game.id,
                                                            serial = player.serial,
                                                            seat = player.seat))
        game.reset()
        game.name = "*REPLAY*"
        game.setVariant(variant)
        game.setBettingStructure(betting_structure)
        game.setTime(time)
        game.setHandsCount(hands_count)
        game.setLevel(level)
        game.hand_serial = hand
        for serial in player_list:
            game.addPlayer(serial)
            game.getPlayer(serial).money = serial2chips[serial]
            game.sit(serial)
        if self.isJoined(client):
            client.join(self)
        else:
            self.joinPlayer(client, client.getSerial())
        serial = client.getSerial()
        cache = self.createCache()
        for packet in self.history2packets(history, game.id, cache):
            if packet.type == PACKET_POKER_PLAYER_CARDS and packet.serial == serial:
                packet.cards = cache["pockets"][serial].toRawList()
            if packet.type == PACKET_POKER_PLAYER_LEAVE:
                continue
            client.sendPacketVerbose(packet)

    def isJoined(self, client):
        return client in self.observers or self.serial2client.has_key(client.getSerial())

    def isSeated(self, client):
        return self.isJoined(client) and self.game.isSeated(client.getSerial())

    def isSit(self, client):
        return self.isSeated(client) and self.game.isSit(client.getSerial())

    def isSerialObserver(self, serial):
        return serial in [ client.getSerial() for client in self.observers ]
    
    def isOpen(self):
        return self.game.is_open

    def isRunning(self):
        return self.game.isRunning()

    def seated2observer(self, client):
        del self.serial2client[client.getSerial()]
        self.observers.append(client)

    def observer2seated(self, client):
        self.observers.remove(client)
        self.serial2client[client.getSerial()] = client
        
    def quitPlayer(self, client, serial):
        game = self.game
        if self.isSit(client):
            if self.isOpen():
                game.sitOutNextTurn(serial)
            game.autoPlayer(serial)
        self.update()
        if self.isSeated(client):
            #
            # If not on a closed table, stand up
            #
            if self.isOpen():
                if client.removePlayer(self, serial):
                    self.seated2observer(client)
                    self.factory.leavePlayer(serial, game.id, self.currency_serial)
                else:
                    self.update()
            else:
                client.message("cannot quit a closed table, request ignored")
                return False

        if self.isJoined(client):
            #
            # The player is no longer connected to the table
            #
            self.destroyPlayer(client, serial)

        return True

    def kickPlayer(self, serial):
        game = self.game

        player = game.getPlayer(serial)
        seat = player and player.seat
        
        if not game.removePlayer(serial):
            print " *ERROR* kickPlayer did not succeed in removing player %d from game %d" % ( serial, game.id )
            return

        self.factory.leavePlayer(serial, game.id, self.currency_serial)

        if self.serial2client.has_key(serial):
            self.seated2observer(self.serial2client[serial])

        self.broadcast(PacketPokerPlayerLeave(game_id = game.id,
                                              serial = serial,
                                              seat = seat))

    def disconnectPlayer(self, client, serial):
        game = self.game

        if self.isSeated(client):
            game.getPlayer(serial).getUserData()['ready'] = True
            if self.isOpen():
                #
                # If not on a closed table, stand up.
                #
                if client.removePlayer(self, serial):
                    self.seated2observer(client)
                    self.factory.leavePlayer(serial, game.id, self.currency_serial)
                else:
                    self.update()
            else:
                #
                # If on a closed table, the player
                # will stay at the table, he does not
                # have the option to leave.
                #
                pass
                
        if self.isJoined(client):
            #
            # The player is no longer connected to the table
            #
            self.destroyPlayer(client, serial)

        return True

    def leavePlayer(self, client, serial):
        game = self.game
        if self.isSit(client):
            if self.isOpen():
                game.sitOutNextTurn(serial)
            game.autoPlayer(serial)
        self.update()
        if self.isSeated(client):
            #
            # If not on a closed table, stand up
            #
            if self.isOpen():
                if client.removePlayer(self, serial):
                    self.seated2observer(client)
                    self.factory.leavePlayer(serial, game.id, self.currency_serial)
                else:
                    self.update()
            else:
                client.error("cannot leave a closed table")
                client.PacketPokerError(game_id = game.id,
                                        serial = serial,
                                        other_type = PACKET_POKER_PLAYER_LEAVE,
                                        code = PacketPokerPlayerLeave.TOURNEY,
                                        message = "Cannot leave tournament table")
                return False

        return True
        
    def movePlayer(self, client, serial, to_game_id):
        game = self.game
        #
        # We are safe because called from within the server under
        # controlled circumstances.
        #

        money = game.serial2player[serial].money

        sit_out = self.movePlayerFrom(serial, to_game_id)
        if client:
            self.destroyPlayer(client, serial)

        other_table = self.factory.getTable(to_game_id)
        if client:
            other_table.serial2client[serial] = client

        money_check = self.factory.movePlayer(serial, game.id, to_game_id)
        if money_check != money:
            print " *ERROR* movePlayer: player %d money %d in database, %d in memory" % ( serial, money_check, money )

        if client:
            client.join(other_table)
        other_table.movePlayerTo(serial, money, sit_out)
        other_table.sendNewPlayerInformation(serial)
        if self.factory.verbose:
            print "player %d moved from table %d to table %d" % ( serial, game.id, to_game_id )

    def sendNewPlayerInformation(self, serial):
        packets = self.newPlayerInformation(serial)
        self.broadcast(packets)

    def newPlayerInformation(self, serial):
        player_info = self.getPlayerInfo(serial)
        game = self.game
        player = game.getPlayer(serial)
        if self.factory.verbose > 1:
            print "about player %d" % serial
        nochips = 0
        packets = [
            PacketPokerPlayerArrive(game_id = game.id,
                                    serial = serial,
                                    name = player_info.name,
                                    url = player_info.url,
                                    outfit = player_info.outfit,
                                    blind = player.blind,
                                    remove_next_turn = player.remove_next_turn,
                                    sit_out = player.sit_out,
                                    sit_out_next_turn = player.sit_out_next_turn,
                                    auto = player.auto,
                                    auto_blind_ante = player.auto_blind_ante,
                                    wait_for = player.wait_for,
                                    seat = player.seat),
            PacketPokerSeats(game_id = game.id, seats = game.seats()),
            PacketPokerPlayerChips(game_id = game.id,
                                   serial = serial,
                                   bet = nochips,
                                   money = game.getPlayer(serial).money),
            ]
        return packets

    def movePlayerTo(self, serial, money, sit_out):
        game = self.game
        game.open()
        game.addPlayer(serial)
        player = game.getPlayer(serial)
        player.setUserData(pokeravatar.DEFAULT_PLAYER_USER_DATA.copy())
        player.money = money
        player.buy_in_payed = True
        game.sit(serial)
        game.autoBlindAnte(serial)
        if sit_out: game.sitOut(serial)
        game.close()

    def movePlayerFrom(self, serial, to_game_id):
        game = self.game
        player = game.getPlayer(serial)
        self.broadcast(PacketPokerTableMove(game_id = game.id,
                                            serial = serial,
                                            to_game_id = to_game_id,
                                            seat = player.seat))
        sit_out = game.isSitOut(serial)
        game.removePlayer(serial)
        return sit_out

    def possibleObserverLoggedIn(self, client, serial):
        game = self.game
        if not game.getPlayer(serial):
            return False
        self.observer2seated(client)
        game.comeBack(serial)
        return True
            
    def joinPlayer(self, client, serial):
        game = self.game
        #
        # Silently do nothing if already joined
        #
        if self.isJoined(client):
            return True

        if len(client.tables) >= self.factory.simultaneous:
            if self.factory.verbose:
                print " *ERROR* joinPlayer: %d seated at %d tables (max %d)" % ( serial, len(client.tables), self.factory.simultaneous )
            return False
        
        #
        # Player is now an observer, unless he is seated
        # at the table.
        #
        client.join(self)
        if not self.game.isSeated(client.getSerial()):
            self.observers.append(client)
        else:
            self.serial2client[serial] = client
        #
        # If it turns out that the player is seated
        # at the table already, presumably because he
        # was previously disconnected from a tournament
        # or an ongoing game.
        #
        if self.isSeated(client):
            #
            # Sit back immediately, as if we just seated
            #
            game.comeBack(serial)
            
        return True

    def seatPlayer(self, client, serial, seat):
        game = self.game
        if not self.isJoined(client):
            client.error("player %d can't seat before joining" % serial)
            return False
        #
        # Do nothing if already seated
        #
        if self.isSeated(client):
            print "player %d is already seated" % serial
            return False

        if not game.canAddPlayer(serial):
            client.error("table refuses to seat player %d" % serial)
            return False

        if seat != -1 and seat not in game.seats_left:
            client.error("table refuses to seat player %d at seat %d" % ( serial, seat ))
            return False

        amount = 0
        if self.transient:
            amount = game.buyIn()
            
        if not self.factory.seatPlayer(serial, game.id, amount):
            return False

        self.observer2seated(client)

        client.addPlayer(self, seat)
        if amount > 0:
            client.setMoney(self, amount)

        return True

    def sitOutPlayer(self, client, serial):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't sit out before getting a seat" % serial)
            return False
        #
        # Silently do nothing if already sit out
        #
        if not self.isSit(client):
            return True

        client.sitOutPlayer(self, serial)
        return True

    def chatPlayer(self, client, serial, message):
        self.broadcast(PacketPokerChat(game_id = self.game.id,
                                       serial = serial,
                                       message = message + "\n"))

    def autoBlindAnte(self, client, serial, auto):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't set auto blind/ante before getting a seat" % serial)
            return False
        return client.autoBlindAnte(self, serial, auto)
        
    def muckAccept(self, client, serial):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't accept muck before getting a seat" % serial)
            return False
        return game.muck(serial, want_to_muck = True)

    def muckDeny(self, client, serial):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't deny muck before getting a seat" % serial)
            return False
        return game.muck(serial, want_to_muck = False)
    
    def sitPlayer(self, client, serial):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't sit before getting a seat" % serial)
            return False

        return client.sitPlayer(self, serial)
        
    def destroyPlayer(self, client, serial):
        if client in self.observers:
            self.observers.remove(client)
        else:
            del self.serial2client[serial]
        del client.tables[self.game.id]

    def buyInPlayer(self, client, amount):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't bring money to a table before getting a seat" % client.getSerial())
            return False

        if client.getSerial() in game.serialsPlaying():
            client.error("player %d can't bring money while participating in a hand" % client.getSerial())
            return False

        if self.transient:
            client.error("player %d can't bring money to a transient table" % client.getSerial())
            return False

        amount = self.factory.buyInPlayer(client.getSerial(), game.id, self.currency_serial, max(amount, game.buyIn()))
        return client.setMoney(self, amount)
        
    def rebuyPlayerRequest(self, client, amount):
        game = self.game
        if not self.isSeated(client):
            client.error("player %d can't rebuy to a table before getting a seat" % client.getSerial())
            return False

        serial = client.getSerial()
        player = game.getPlayer(serial)
        if not player.isBuyInPayed():
            client.error("player %d can't rebuy before paying the buy in" % serial)
            return False

        if self.transient:
            client.error("player %d can't rebuy on a transient table" % serial)
            return False

        maximum = game.maxBuyIn() - game.getPlayerMoney(serial)
        if maximum <= 0:
            client.error("player %d can't bring more money to the table" % serial)
            return False

        if amount == 0:
            amount = game.buyIn()
            
        amount = self.factory.buyInPlayer(serial, game.id, self.currency_serial, min(amount, maximum))

        if amount == 0:
            client.error("player %d is broke and cannot rebuy" % serial)
            return False
        
        if not game.rebuy(serial, amount):
            client.error("player %d rebuy denied" % serial)
            return False

        self.broadcast(PacketPokerRebuy(game_id = game.id,
                                        serial = serial,
                                        amount = amount))
        return True
        
    def playerWarningTimer(self, serial):
        game = self.game
        info = self.timer_info
        if game.isRunning() and serial == game.getSerialInPosition():
            timeout = self.playerTimeout / 2;
            #
            # Compensate the communication lag by always giving the client
            # an extra 2 seconds to react. The warning says that there only is
            # N seconds left but the server will actually timeout after N + 2
            # seconds.
            #
            if timeout > 2:
                self.broadcast(PacketPokerTimeoutWarning(game_id = game.id,
                                                         serial = serial,
                                                         timeout = timeout - 2))
            info["playerTimeout"] = reactor.callLater(timeout, self.playerTimeoutTimer, serial)
        else:
            self.updatePlayerTimers()

    def playerTimeoutTimer(self, serial):
        if self.factory.verbose:
            print "player %d times out" % serial
        game = self.game
        if game.isRunning() and serial == game.getSerialInPosition():
            if self.timeout_policy == "sitOut":
                game.sitOutNextTurn(serial)
                game.autoPlayer(serial)
            elif self.timeout_policy == "fold":
                game.autoPlayer(serial)
                self.broadcast(PacketPokerAutoFold(game_id = game.id,
                                                   serial = serial))
            else:
                print " *ERROR* unknown timeout_policy %s" % self.timeout_policy
            self.broadcast(PacketPokerTimeoutNotice(game_id = game.id,
                                                    serial = serial))
            self.update()
        else:
            self.updatePlayerTimers()
        
    def muckTimeoutTimer(self):
        if self.factory.verbose:
            print "muck timed out"
        # timer expires, force muck on muckables not responding
        for serial in self.game.muckable_serials:
            self.game.muck(serial, want_to_muck = True)
        self.cancelMuckTimer()
        self.update()
        
    def cancelMuckTimer(self):
        info = self.timer_info
        timer = info["muckTimeout"]
        if timer != None:
            if timer.active():
                timer.cancel()
            info["muckTimeout"] = None
    
    def cancelPlayerTimers(self):
        info = self.timer_info

        timer = info["playerTimeout"]
        if timer != None:
            if timer.active():
                timer.cancel()
            info["playerTimeout"] = None
        info["playerTimeoutSerial"] = 0
        
    def updateTimers(self, history = ()):
        self.updateMuckTimer(history)
        self.updatePlayerTimers()
        
    def updateMuckTimer(self, history):
        for event in history:
            type = event[0]            
            if type == "muck":
                self.cancelMuckTimer()
                self.timer_info["muckTimeout"] = reactor.callLater(self.muckTimeout, self.muckTimeoutTimer)
    
    def updatePlayerTimers(self):
        game = self.game
        info = self.timer_info

        timer = info["playerTimeout"]
        if game.isRunning():
            serial = game.getSerialInPosition()
            #
            # Any event in the game resets the player timeout
            #
            if ( info["playerTimeoutSerial"] != serial or
                 len(game.historyGet()) > self.history_index ):
                if timer != None and timer.active():
                    timer.cancel()

                timer = reactor.callLater(self.playerTimeout / 2, self.playerWarningTimer, serial)
                info["playerTimeout"] = timer
                info["playerTimeoutSerial"] = serial
        else:
            #
            # If the game is not running, cancel the previous timeout
            #
            self.cancelPlayerTimers()

