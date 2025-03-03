import pygame
from Setting import *
#睡觉可以恢复所有体力这些
class Transition:
	def __init__(self,  player):
		
		# 设置
		self.display_surface = pygame.display.get_surface()

		self.player = player

		# 道具图片
		self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.color = 255
		self.speed = -2

	def play(self):
		self.color += self.speed
		if self.color <= 0:
			self.speed *= -1
			self.color = 0

		if self.color > 255:
			self.color = 255
			self.player.sleep = False
			self.speed = -2

		self.image.fill((self.color,self.color,self.color))
		self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
#-------------到此为止-----------------