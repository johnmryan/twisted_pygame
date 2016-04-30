# name: Max Walsh, Jack Ryan
# date: 5/4/16


# PORT1: 40028
# PORT2: 40046

import sys
import os
import math
import pygame
from pygame.locals import *
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from mario_game import MarioKart
from twisted.internet.task import LoopingCall

GAME_SERVER = 'student02.cse.nd.edu'
SEND_PORT1 = 40028
SEND_PORT2 = 40046
#server receives on
# 40028
# 40046

RECEIVE_PORT1 = 9575
#RECEIVE_PORT2 = 9576
#SERVER sends on
#9575
#9576


class Player(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs

class receiveConnection(Protocol):
    def __init__(self, sendConn):
        self.sendConn = sendConn

    def dataReceived(self, data):
        print 'data:' + str(data)

    def connectionMade(self):
        print 'Receive Connection made'

    def connectionLost(self, reason):
        print 'lost connection'
        reactor.stop()

    def sendData(self, data):
        print 'send:'

class ReceiveConnectionFactory(ClientFactory):
    #def __init__(self, sendConn):
        #self.sendConn = sendConn

    def buildProtocol(self, addr):
        return ReceiveConnection(self.sendConn)

class SendConnection(Protocol):
    def __init__(self, game):
        self.game = game
        self.game.getOutgoingConnection(self)

    def dataReceived(self, data):
        print 'received data' + str(data)

    def connectionMade(self):
        print "connected as Player 1"
        #3try:
        reactor.listenTCP(RECEIVE_PORT1, ReceiveConnectionFactory())
        #except Exception as ex:

    def connectionLost(self, reason):
        print 'lost connection:'
        reactor.stop()
    def sendData(self, data):
        print 'sending: '+str(data)
        self.transport.write(data)

class SendConnFactory(ClientFactory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        return SendConnection(self.game)

    def clientConnectionFailed(self, connector, reason):
        print 'connect failed, connecting as Player 2'
    #player = 2
        reactor.connectTCP(GAME_SERVER, SEND_PORT2, SendConnFactory())

if __name__ == "__main__":
    game = MarioKart(1)
    
    DESIRED_FPS = 30.0
    
    tick = LoopingCall(game.game_tick)
    tick.start(1.0 / DESIRED_FPS)
    sendConnFactory = SendConnFactory(game)
    reactor.connectTCP(GAME_SERVER, int(SEND_PORT1), sendConnFactory)
    #reactor.listenTCP(RECEIVE_PORT1, ReceiveConnectionFactory())
    reactor.run()

