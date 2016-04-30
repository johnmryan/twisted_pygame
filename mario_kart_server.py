# Jack Ryan, Max Walsh
# 4/29/16
# mario_kart_server.py

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

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
		reactor.listenTCP(PLAYER2_PORT, Player2_IncomingConnFactory())



	def connectionLost(self, reason):
		print "Lost connection from player 1:", str(reason)

	def startForwarding(self):
		# start forwarding the player 1 data
		print "sendData"

	def sendData(self, data):
		# not sure
		print "sendData"

class Player2_IncomingConnFactory(Factory):
	def buildProtocol(self, addr):
		return Player2_IncomingConnection(addr)

class Player2_IncomingConnection(Protocol):
	def __init__(self, addr):
		self.addr = addr
		PLAYER2_HOST = addr.host

	def dataReceived(self, data):
		# data received from player 2
		dq.put(data)

	def connectionMade(self):
		print "Connection receieved from player 2"
		# initiate outgoing to player 1
		reactor.connectTCP(PLAYER1_HOST, PLAYER1_OPEN_PORT, Player1_OutgoingConnFactory())

	def connectionLost(self, reason):
		print "Lost connection from player 2:", str(reason)

	def startForwarding(self):
		# start forwarding the player 2 data
		print "sendData"

	def sendData(self, data):
		# not sure
		print "sendData"

############ Outgoing Player Connections #############
class Player1_OutgoingConnFactory(ClientFactory):
	def buildProtocol(self, addr):
		return Player1_OutgoingConnection()

class Player1_OutgoingConnection(Protocol):
	def __init__(self):
		pass

	def connectionMade(self):
		print "Outgoing connection made to player 1"
		# initiate outgoing connection
		reactor.connectTCP(PLAYER2_HOST, PLAYER2_OPEN_PORT, Player2_OutgoingConnFactory())

	def connectionLost(self, reason):
		print "Lost outgoing connection from player 1:", str(reason)

class Player2_OutgoingConnFactory(ClientFactory):
	def buildProtocol(self, addr):
		return Player2_OutgoingConnection()

class Player2_OutgoingConnection(Protocol):
	def __init__(self):
		pass

	def connectionMade(self):
		print "Outgoing connection made to player 2"
		print "Ready to begin game!"

	def connectionLost(self, reason):
		print "Lost outgoing connection from player 2:", str(reason)

if __name__ == "__main__":
	reactor.listenTCP(PLAYER1_PORT, Player1_IncomingConnFactory())
	reactor.run()
