# Jack Ryan, Max Walsh
# 4/29/16
# mario_kart_server.py

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
import pygame
from pygame.locals import *
import cPickle as pickle
# use import pickle to debug

###################    Globals   ######################
PLAYER1_PORT = 40028
#PLAYER1_OPEN_PORT = 9575
PLAYER1_HOST = ""
#PLAYER1_CONNECT = 0

PLAYER2_PORT = 40046
#PLAYER2_OPEN_PORT = 9576
PLAYER2_HOST = ""

# Global deferred queue, handles input from both players
dq = DeferredQueue()

FPS = 30.0

class GameState:
	#def main(self):
	def __init__(self):
		#pygame.init()
		self.size = self.width, self.height = 1888, 1648
		self.black = 0, 0, 0

		self.playerOne = 0, 0 # Location
		self.playerTwo = 0, 0

		self.finishLineStart = (500, 900)
		self.finishLineEnd = (500, 1000)

	def game_tick(self):
		#print 'game_tick'
		pass

	def decode_data(self, data):
		print data
		dataList = data.split(":")
		#print dataList[0]

gs = GameState()

############ Incoming Player Connections #############
class Player1_ConnFactory(Factory):
	def buildProtocol(self, addr):
		return Player1_Connection(addr)

class Player1_Connection(Protocol):
	def __init__(self, addr):
		self.addr = addr
		PLAYER1_HOST = addr.host

	def dataReceived(self, data):
		# data received from player 1
		#dq.put(data)
		print str(data)

	def connectionMade(self):
		print "Connection receieved from player 1"
		# listen for player 2
		reactor.listenTCP(PLAYER2_PORT, Player2_ConnFactory(self))


	def connectionLost(self, reason):
		print "Lost connection from player 1:", str(reason)

	def startForwarding(self):
		# start forwarding the player 1 data
		print "sendData"

	def sendData(self, data):
		# not sure
		print "sendData P1"

class Player2_ConnFactory(Factory):
	def __init__(self, player1_conn):
		self.player1_conn = player1_conn

	def buildProtocol(self, addr):
		return Player2_Connection(addr, self.player1_conn)

class Player2_Connection(Protocol):
	def __init__(self, addr, player1_conn):
		self.addr = addr
		print addr
		PLAYER2_HOST = addr.host
		self.player1_conn = player1_conn

	def dataReceived(self, data):
		# data received from player 2
		print str(data)
		dq.put(data)

	def connectionMade(self):
		print "Connection receieved from player 2"
		print "ready to begin game"
		#self.startForwarding()

	def connectionLost(self, reason):
		print "Lost connection from player 2:", str(reason)

	def startForwarding(self):
		# start forwarding the player 2 data
		print "sendData"
		dq.get().addCallback(gs.decode_data)

	def sendData(self, data):
		# not sure
		print "sendData P2"


if __name__ == "__main__":
	# http://stackoverflow.com/questions/8381850/combining-pygame-and-twisted
	#gs = GameState()
	#tick = LoopingCall(gs.game_tick)
	#tick.start(1.0 / FPS)
	reactor.listenTCP(PLAYER1_PORT, Player1_ConnFactory())
	reactor.run()
