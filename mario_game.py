import sys
import pygame

# Class to handle the pygame, gets data from server and updates accordingly
class MarioKart():
	def __init__(self, playerNum):
		self.isPlayer1 = False
		if playerNum == 1:
			self.isPlayer1 = True
		self.width = 1200
		self.height = 900
		self.size = self.width, self.height
		pygame.init()
		self.screen = pygame.display.set_mode(self.size)
		self.background = pygame.image.load("assets/mario-kart-circuit.png")
		self.background_rect = self.background.get_rect()
		# Mario initialization
		self.marioX = 470
		self.marioY = 455
		self.mario_image = pygame.image.load("assets/mario.png")
		self.mario_image_old = self.mario_image
		self.mario_image = pygame.transform.flip(self.mario_image_old, True, False)
		self.mario_rect = self.mario_image.get_rect()
		self.mario_rect.x = self.marioX
		self.mario_rect.y = self.marioY

		# Yoshi initialization
		self.yoshiX = 500
		self.yoshiY = 460
		
	def game_tick(self):
		pygame.key.set_repeat(1, 20)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key >= 273 and event.key <= 276:
					# this is a movement key
					self.movePlayer(event.key)

			self.screen.blit(self.background, self.background_rect)
			self.screen.blit(self.mario_image, self.mario_rect)
			pygame.display.flip()

	def getOutgoingConnection(self, outgoingConn):
		self.outgoingConn = outgoingConn

	def movePlayer(self, keyNum):
		if self.isPlayer1:
			self.outgoingConn.transport.write("1:" + str(keyNum))
		else:
			self.outgoingConn.transport.write("2:" + str(keyNum))

