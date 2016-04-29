# name: Max Walsh
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

GAME_SERVER = 'student02.cse.nd.edu'
SEND_PORT1 = 40028
SEND_PORT2 = 40046
connectAttempts = 0
#server receives on
# 40028
# 40046

RECEIVE_PORT1 = 9575
RECEIVE_PORT2 = 9576
#SERVER sends on
#9575
#9576



class Player(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.port1 = '40028'
        self.port2 = '40046'
        self.myPort = ''

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
    def __init__(self, sendConn):
        self.sendConn = sendConn

    def buildProtocol(self, addr):
        return ReceiveConnection(self.sendConn)

class SendConnection(Protocol):
    def dataReceived(self, data):
        print 'received data' + str(data)

    def connectionMade(self):
        print "connection made: " #+ str(port)
        reactor.listenTCP(GAME_SERVER, int(RECEIVE_PORT1), ReceiveConnectionFactory(self))
        #self.myPort = port
        #self.transport.write("")

    def connectionLost(self, reason):
        print 'lost connection:'
        reactor.stop()
    def sendData(self, data):
        print 'sending: '+str(data)
        self.transport.write(data)

class SendConnFactry(ClientFactory):
    #def __init__(self):
        #self.connectAttempts = 0

    def buildProtocol(self, addr):
        return SendConnection()

    def clientConnectionFailed(self, connector, reason):
        #print 'couldnt connect||' + str(connector)+ '||' + str(reason)
        #print connectAttempts
        print 'connect failed'
        reactor.stop()
        if connectAttempts < 1:
            print 'why'
            #connectAttempts = connectAttempts + 1
            #reactor.connectTCP(HOST, 40046, SendConnFactry())
            #self.connectAttempts += 1
        else:
            reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP(GAME_SERVER, int(SEND_PORT1), SendConnFactry())
#    reactor.listenTCP(GAME_SERVER, RECEIVE_PORT1, ReceiveConnectionFactory())
    reactor.run()
