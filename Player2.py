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
PORT2 = 40046

class PlayerConnectionFactory(ClientFactory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        return PlayerConnection(self.game)

class PlayerConnection(Protocol):
    def __init__(self, game):
        self.game = game
        self.game.transferConnectionObject(self)

    def dataReceived(self, data):
        print 'data:' + str(data)
		self.handleReceievedData(self, data)

    def connectionMade(self):
        print 'Receive Connection made'

    def connectionLost(self, reason):
        print 'lost connection'
        reactor.stop()

    def sendData(self, data):
        print 'send:'

	def handleReceivedData(self, data):
        obj = json.loads(data)
        self.game.handleData(obj)




if __name__ == "__main__":
    game = MarioKart(2)

    DESIRED_FPS = 30.0
    
    tick = LoopingCall(game.game_tick)
    tick.start(1.0 / DESIRED_FPS)
    reactor.connectTCP(GAME_SERVER, PORT2, PlayerConnectionFactory(game))
    reactor.run()
