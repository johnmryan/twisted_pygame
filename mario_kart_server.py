# Jack Ryan, Max Walsh
# 4/29/16
# mario_kart_server.py

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
import json
# use import pickle to debug

###################    Globals   ######################
PLAYER1_PORT = 40028
PLAYER1_HOST = ""

PLAYER2_PORT = 40046
PLAYER2_HOST = ""

# Global deferred queue, handles input from both players
dq = DeferredQueue()

FPS = 30.0

class GameState:
	#def main(self):
	def __init__(self):
		self.mario_x = 474
		self.mario_y = 134
		self.yoshi_x = 474
		self.yoshi_y = 208
	
		self.boost1_taken = False
		self.boost2_taken = False
		self.boost3_taken = False
		self.boost4_taken = False
		self.mario_speed = 5
		self.yoshi_speed = 5
		self.finishLineStart = (500, 900)
		self.finishLineEnd = (500, 1000)

	def getPlayer1_Connection(self, p1_conn):
		self.player1_Conn = p1_conn

	def getPlayer2_Connection(self, p2_conn):
		self.player2_Conn = p2_conn

	def check_track_bound(self, x, y):
		if x <= 110 or x >= 1070 or y <= 110 or y >= 774:
			return False
		if y >= 250 and y <= 670 and x >= 255 and x <= 920:
			return False
		return True

	def applyBoosts(self):
		if not self.boost1_taken:
			# boost1 is still open for the taking
			if self.mario_x >= 320 and self.mario_x <= 345 and self.mario_y >= 160 and self.mario_y <= 185:
				self.mario_speed += 1
				self.boost1_taken = True
			elif self.yoshi_x >= 320 and self.yoshi_x <= 345 and self.yoshi_y >= 160 and self.yoshi_y <= 185:
				self.yoshi_speed += 1
				self.boost1_taken = True

		if not self.boost2_taken:
			# boost2 is still open for the taking
			if self.mario_x >= 140 and self.mario_x <= 165 and self.mario_y >= 420 and self.mario_y <= 445:
				self.mario_speed += 2
				self.boost2_taken = True
			elif self.yoshi_x >= 140 and self.yoshi_x <= 165 and self.yoshi_y >= 420 and self.yoshi_y <= 445:
				self.yoshi_speed += 2
				self.boost2_taken = True
		
		if not self.boost3_taken:
			# boost4 is still open for the taking
			if self.mario_x >= 530 and self.mario_x <= 555 and self.mario_y >= 710 and self.mario_y <= 735:
				self.mario_speed += 3
				self.boost3_taken = True
			elif self.yoshi_x >= 530 and self.yoshi_x <= 555 and self.yoshi_y >= 710 and self.yoshi_y <= 735:
				self.yoshi_speed += 3
				self.boost3_taken = True
		
		if not self.boost4_taken:
			# boost3 is still open for the taking
			if self.mario_x >= 930 and self.mario_x <= 955 and self.mario_y >= 490 and self.mario_y <= 515:
				self.mario_speed += 4
				self.boost4_taken = True
			elif self.yoshi_x >= 930 and self.yoshi_x <= 955 and self.yoshi_y >= 490 and self.yoshi_y <= 515:
				self.yoshi_speed += 4
				self.boost4_taken = True

	def decode_data(self, data):
		print data
		dataList = data.split(":")
		if dataList[1] == '-1':
			reactor.stop()
			return
		if dataList[0] == '1':
			
			if dataList[1] == '273': # UP
				self.mario_y -= self.mario_speed
			elif dataList[1] == '274': # DOWN
				self.mario_y += self.mario_speed
			elif dataList[1] == '275': # RIGHT
				self.mario_x += self.mario_speed
			elif dataList[1] == '276': # LEFT
				self.mario_x -= self.mario_speed
			if self.check_track_bound(self.mario_x, self.mario_y) == False:
				self.mario_x = 474
				self.mario_y = 134
		elif dataList[0] == '2':
			if dataList[1] == '273': # UP
				self.yoshi_y -= self.yoshi_speed
			elif dataList[1] == '274': # DOWN
				self.yoshi_y += self.yoshi_speed
			elif dataList[1] == '275': # RIGHT
				self.yoshi_x += self.yoshi_speed
			elif dataList[1] == '276': # LEFT
				self.yoshi_x -= self.yoshi_speed
			if self.check_track_bound(self.yoshi_x, self.yoshi_y) == False:
				self.yoshi_x = 474
				self.yoshi_y = 208
		else:
			print'this is working'
		self.applyBoosts()
		string = json.dumps({'mario_x':self.mario_x, 'mario_y':self.mario_y, 'yoshi_x':self.yoshi_x, 'yoshi_y':self.yoshi_y})
		self.player1_Conn.sendData(string)
		self.player2_Conn.sendData(string)
		dq.get().addCallback(gs.decode_data)

gs = GameState()


class Player1_ConnFactory(Factory):
	def buildProtocol(self, addr):
		return Player1_Connection(addr)

class Player1_Connection(Protocol):
	def __init__(self, addr):
		self.addr = addr
		PLAYER1_HOST = addr.host
		#self.player2_conn = ""

	def dataReceived(self, data):
		# data received from player 1
		dq.put(data)
		print str(data)

	def connectionMade(self):
		print "Connection receieved from player 1"
		# listen for player 2
		gs.getPlayer1_Connection(self)
		reactor.listenTCP(PLAYER2_PORT, Player2_ConnFactory(self))
		

	def connectionLost(self, reason):
		print "Lost connection from player 1:", str(reason)

	def startForwarding(self):
		# start forwarding the player 1 data
		print "sendData"
		dq.get().addCallback(gs.decode_data)

	def sendData(self, data):
		# not sure
		print "send P1 data to P2"
		self.transport.write(data)		

	def getPlayer2_Connection(self, player2_conn):
		self.player2_conn = player2_conn

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
		self.player1_conn.getPlayer2_Connection(self)
		gs.getPlayer2_Connection(self)
		self.startForwarding()

	def connectionLost(self, reason):
		print "Lost connection from player 2:", str(reason)

	def startForwarding(self):
		# start forwarding the player 2 data
		print "sendData"
		#dq.get().addCallback(gs.decode_data)
		dq.get().addCallback(gs.decode_data)

	def sendData(self, data):
		# not sure
		#print "sendData P2"
		print 'send P2 data to P1'
		self.transport.write(data)


if __name__ == "__main__":
	# http://stackoverflow.com/questions/8381850/combining-pygame-and-twisted
	#gs = GameState()
	#tick = LoopingCall(gs.game_tick)
	#tick.start(1.0 / FPS)
	reactor.listenTCP(PLAYER1_PORT, Player1_ConnFactory())
	reactor.run()
