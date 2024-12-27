import pygame, sys
from Setting import *
from Level import Level
from Menu import start_menu
class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('UnderTruth')
		self.clock = pygame.time.Clock()
		self.start_menu=start_menu(self.screen)
		if self.start_menu == 1:
			self.level=Level()
		elif self.start_menu == 2:
			pass
		elif self.start_menu == 3:
			pygame.quit()
			sys.exit()


	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()