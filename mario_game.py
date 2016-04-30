import sys
import pygame

# Class to handle the pygame, gets data from server and updates accordingly
class MarioKart():
	def __init__(self):
		self.width = 1200
		self.height = 900
		self.size = self.width, self.height
		pygame.init()
		self.screen = pygame.display.set_mode(self.size)
		self.background = pygame.image.load("assets/mario-kart-circuit.png")
		self.background_rect = self.background.get_rect()
		
	def game_tick(self):
		pygame.key.set_repeat(1, 20)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			self.screen.blit(self.background, self.background_rect)
			pygame.display.flip()
