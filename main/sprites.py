import pygame
from Setting import *

class Generic(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z=z#z轴1坐标，用于分层
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2,-self.rect.height * 0.75)#负号就是缩小,数字要自己调
		
		
class Interaction(Generic):#交互
	def __init__(self, pos, size, groups, name):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.name = name
		

class Water(Generic):
	def __init__(self, pos, frames, groups):

		#动画设置
		self.frames = frames
		self.frame_index = 0

		# 群组设置
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups, 
				z = LAYERS['water']) 

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		self.animate(dt)

class WildFlower(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Tree(Generic):
	def __init__(self, pos, surf, groups, name):
		super().__init__(pos, surf, groups)

class house(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf,groups)
		# self.image=pygame.transform.scale(self.image,(200,300))
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height*0.6 )

class boss(Generic):#boss坐标大概为（993，448）
	def __init__(self, pos, frames, groups):
		#动画设置
		self.frames = frames
		self.frame_index = 0
	# 群组设置
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups) 

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
		self.image=pygame.transform.scale(self.image,(90,120))

	def update(self,dt):
		self.animate(dt)