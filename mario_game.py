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
		self.marioX = 474
		self.marioY = 134
		self.mario_image = pygame.image.load("assets/mario.png")
		self.mario_image_old = self.mario_image
		self.mario_image = pygame.transform.flip(self.mario_image_old, True, False)
		self.mario_rect = self.mario_image.get_rect()
		self.mario_rect.x = self.marioX
		self.mario_rect.y = self.marioY

		# Yoshi initialization
		self.yoshiX = 474
		self.yoshiY = 208
		self.yoshi_image = pygame.image.load("assets/yoshi.png")
		self.yoshi_image_old = self.yoshi_image
		self.yoshi_image = pygame.transform.flip(self.yoshi_image_old, True, False)
		self.yoshi_rect = self.yoshi_image.get_rect()
		self.yoshi_rect.x = self.yoshiX
		self.yoshi_rect.y = self.yoshiY

		# Boost arrows
		self.boost1_x = 320
		self.boost1_y = 160
		self.boost1_image = pygame.image.load("assets/boost_arrow.png")
		self.boost1_image_old = self.boost1_image
		self.boost1_image = pygame.transform.flip(self.boost1_image_old, True, False)
		self.boost1_rect = self.boost1_image.get_rect()
		self.boost1_rect.x = self.boost1_x
		self.boost1_rect.y = self.boost1_y

		self.boost2_x = 140
		self.boost2_y = 420
		self.boost2_image = pygame.image.load("assets/boost_arrow.png")
		self.boost2_image_old = self.boost2_image
		self.boost2_image = pygame.transform.rotate(self.boost2_image_old, 270.)
		self.boost2_rect = self.boost2_image.get_rect()
		self.boost2_rect.x = self.boost2_x
		self.boost2_rect.y = self.boost2_y

		self.boost3_x = 930
		self.boost3_y = 490
		self.boost3_image = pygame.image.load("assets/boost_arrow.png")
		self.boost3_image_old = self.boost3_image
		self.boost3_image = pygame.transform.rotate(self.boost3_image_old, 90.)
		self.boost3_rect = self.boost3_image.get_rect()
		self.boost3_rect.x = self.boost3_x
		self.boost3_rect.y = self.boost3_y

		self.boost4_x = 530
		self.boost4_y = 710
		self.boost4_image = pygame.image.load("assets/boost_arrow.png")
		self.boost4_image_old = self.boost4_image
		self.boost4_rect = self.boost4_image.get_rect()
		self.boost4_rect.x = self.boost4_x
		self.boost4_rect.y = self.boost4_y

		# Winner images
		self.mario_won = False
		self.mario_winner_image = pygame.image.load("assets/mario_winner.png")
		self.mario_winner_rect = self.mario_winner_image.get_rect()
		self.mario_winner_rect.x = 474
		self.mario_winner_rect.y = 230
		
		self.yoshi_won = False
		self.yoshi_winner_image = pygame.image.load("assets/yoshi_winner.png")
		self.yoshi_winner_rect = self.yoshi_winner_image.get_rect()
		self.yoshi_winner_rect.x = 474
		self.yoshi_winner_rect.y = 230
		
		pygame.key.set_repeat(1, 30)
		
	def game_tick(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.sendData(-1)
			if event.type == pygame.KEYDOWN:
				if event.key >= 273 and event.key <= 276:
					# this is a movement key
					self.sendData(event.key)

		self.screen.blit(self.background, self.background_rect)
		self.screen.blit(self.mario_image, self.mario_rect)
		self.screen.blit(self.yoshi_image, self.yoshi_rect)
		self.screen.blit(self.boost1_image, self.boost1_rect)
		self.screen.blit(self.boost2_image, self.boost2_rect)
		self.screen.blit(self.boost3_image, self.boost3_rect)
		self.screen.blit(self.boost4_image, self.boost4_rect)
		if self.yoshi_won:
			self.screen.blit(self.yoshi_winner_image, self.yoshi_winner_rect)
		if self.mario_won:
			self.screen.blit(self.mario_winner_image, self.mario_winner_rect)
		pygame.display.flip()

	def sendData(self, keyNum):
		if self.isPlayer1:
			self.outgoingConn.transport.write("1:" + str(keyNum))
		else:
			self.outgoingConn.transport.write("2:" + str(keyNum))

	def transferConnectionObject(self, obj):
		self.outgoingConn = obj

	def handleData(self, data):
		self.mario_rect.x = int(data['mario_x'])
		self.mario_rect.y = int(data['mario_y'])
		self.yoshi_rect.x = int(data['yoshi_x'])
		self.yoshi_rect.y = int(data['yoshi_y'])
		if data['yoshi_won'] == "True":
			self.yoshi_won = True
		if data['mario_won'] == "True":
			self.mario_won = True
		
		
