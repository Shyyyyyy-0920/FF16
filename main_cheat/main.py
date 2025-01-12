import pygame, sys
from Setting import *
from selected import selected

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('UnderTruth')
		self.clock = pygame.time.Clock()
		self.flag=selected()
		#初始化混音器
		pygame.mixer.init()
		pygame.mixer.music.load('../assets/audio/start_menu.wav')
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(loops=-1)  # 循环播放

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000
			self.flag.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
#---------到此为止------------
