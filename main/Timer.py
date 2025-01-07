import pygame
#转换函数，用来调节何时启动
class Timer:
	def __init__(self,duration,func = None):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duration:#这里跟activate函数的区别就是不断调用
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()

#-------------到此为止-----------------