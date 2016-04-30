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
PLAYER1_OPEN_PORT = 9575
PLAYER1_HOST = ""
PLAYER1_CONNECT = 0

PLAYER2_PORT = 40046
PLAYER2_OPEN_PORT = 9576
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
class Player1_IncomingConnFactory(Factory):
	def buildProtocol(self, addr):
		return Player1_IncomingConnection(addr)

class Player1_IncomingConnection(Protocol):
	def __init__(self, addr):
		self.addr = addr
		PLAYER1_HOST = addr.host

	def dataReceived(self, data):
		# data received from player 1
		dq.put(data)

	def connectionMade(self):
		print "Connection receieved from player 1"
		# listen for player 2
		reactor.listenTCP(PLAYER2_PORT, Player2_IncomingConnFactory(self))


	def connectionLost(self, reason):
		print "Lost connection from player 1:", str(reason)

	def startForwarding(self):
		# start forwarding the player 1 data
		print "sendData"

	def sendData(self, data):
		# not sure
		print "sendData P1"

class Player2_IncomingConnFactory(Factory):
	def __init__(self, player1_incoming_conn):
		self.player1_incoming_conn = player1_incoming_conn

	def buildProtocol(self, addr):
		return Player2_IncomingConnection(addr, self.player1_incoming_conn)

class Player2_IncomingConnection(Protocol):
	def __init__(self, addr, player1_incoming_conn):
		self.addr = addr
		print addr
		PLAYER2_HOST = addr.host
		self.player1_incoming_conn = player1_incoming_conn

	def dataReceived(self, data):
		# data received from player 2
		dq.put(data)

	def connectionMade(self):
		print "Connection receieved from player 2"
		# initiate outgoing to player 1
		reactor.connectTCP(PLAYER1_HOST, PLAYER1_OPEN_PORT, Player1_OutgoingConnFactory(self.player1_incoming_conn, self))
		self.startForwarding()

	def connectionLost(self, reason):
		print "Lost connection from player 2:", str(reason)

	def startForwarding(self):
		# start forwarding the player 2 data
		print "sendData"
		dq.get().addCallback(gs.decode_data)

	def sendData(self, data):
		# not sure
		print "sendData P2"

############ Outgoing Player Connections #############
class Player1_OutgoingConnFactory(ClientFactory):
	def __init__(self, player1_incoming_conn, player2_incoming_conn):
		self.player1_incoming_conn = player1_incoming_conn
		self.player2_incoming_conn = player2_incoming_conn

	def buildProtocol(self, addr):
		return Player1_OutgoingConnection(self.player1_incoming_conn, self.player2_incoming_conn)

class Player1_OutgoingConnection(Protocol):
	def __init__(self, player1_incoming_conn, player2_incoming_conn):
		self.player1_incoming_conn = player1_incoming_conn
		self.player2_incoming_conn = player2_incoming_conn

	def connectionMade(self):
		print "Outgoing connection made to player 1"
		# initiate outgoing connection
		reactor.connectTCP(PLAYER2_HOST, PLAYER2_OPEN_PORT, Player2_OutgoingConnFactory(self.player2_incoming_conn))

	def connectionLost(self, reason):
		print "Lost outgoing connection from player 1:", str(reason)

class Player2_OutgoingConnFactory(ClientFactory):
	def __init__(self, player2_incoming_conn):
		self.player2_incoming_conn = player2_incoming_conn

	def buildProtocol(self, addr):
		return Player2_OutgoingConnection(self.player2_incoming_conn)

class Player2_OutgoingConnection(Protocol):
	def __init__(self, player2_incoming_conn):
		self.player2_incoming_conn = player2_incoming_conn

	def connectionMade(self):
		print "Outgoing connection made to player 2"
		print "Ready to begin game!"
		df.get().addCallback(gs.decode_data)

	def connectionLost(self, reason):
		print "Lost outgoing connection from player 2:", str(reason)

	def sendData(self, data):
		print 'send: ' + str(data)

if __name__ == "__main__":
	# http://stackoverflow.com/questions/8381850/combining-pygame-and-twisted
	#gs = GameState()
	#tick = LoopingCall(gs.game_tick)
	#tick.start(1.0 / FPS)
	reactor.listenTCP(PLAYER1_PORT, Player1_IncomingConnFactory())
	reactor.run()
