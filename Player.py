import pygame
from Setting import *
from support import *
from Timer import Timer
import random
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group,collision_sprites,interaction,toggle_shop):
		super().__init__(group)

		self.import_assets()
		self.status = 'down_idle'  #用于判断现在是那组图片
		self.frame_index = 0#用于索引那一组图片的第几个

		 # 普通部分的设置
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z=LAYERS['main']

		
		#运动方面的设置
		self.direction = pygame.math.Vector2()#用向量来表示移动方向
		self.pos = pygame.math.Vector2(self.rect.center)#让人物在移动的同时更新矩形框
		self.speed = 200#玩家速度

		#碰撞部分的逻辑
		
		self.hitbox = self.rect.copy().inflate((-126,-70))#inflate所做的就是改变矩形的尺寸，同时保持它围绕wall center，传入的元祖为（宽度，高度）
		self.collision_sprites = collision_sprites
        
		# 时钟部分
		self.timers = {
			'tool use': Timer(350,self.use_tool),
			'tool switch': Timer(200),
			'seed use': Timer(350,self.use_seed),
			'seed switch': Timer(200),
		}

		# 工具栏
		self.tools = ['hoe','axe','water']
		self.tool_index = 0
		self.selected_tool = self.tools[self.tool_index]

		# 播种子
		self.seeds = ['corn', 'tomato']
		self.seed_index = 0
		self.selected_seed = self.seeds[self.seed_index]

		#库存物品
		self.item_inventory = {
			'wood':   20,
			'apple':  20,
			'corn':   20,
			'tomato': 20
		}

		self.seed_inventory = {
		'corn': 5,
		'tomato': 5
		}

		#库存
		self.money=200

		# interaction

		self.interaction = interaction
		self.sleep = False

		self.toggle_shop = toggle_shop


        
	def use_tool(self):
		pass
	def use_seed(self):
		pass

	def import_assets(self):
		#创建一个字典,必须是字典，否则无法让对应的动作显示对应的动画
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

		for animation in self.animations.keys():
			full_path = '../graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)
	def animate(self,dt):
		self.frame_index += 4*dt#帧速率，但是会返回一个浮点数，下面这个记得转换
		#由于每个动作组都有有限的数量,要让动画只会循环这四个
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0
		self.image = self.animations[self.status][int(self.frame_index)]#加载之前存在字典里的图片
	
	def input(self):
		keys = pygame.key.get_pressed()
        
		if not self.timers['tool use'].active and not self.sleep:
		    # directions 
			if keys[pygame.K_w]:
				self.direction.y = -1#这些都表示某个方向向量
				self.status = 'up'#这里就可以展示特定的动画
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

		    #道具使用
			if keys[pygame.K_SPACE]:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# 更换道具
			if keys[pygame.K_q] and not self.timers['tool switch'].active:
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
				self.selected_tool = self.tools[self.tool_index]

			# 种子部分的使用
			if keys[pygame.K_LCTRL]:
				self.timers['seed use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# 更换种子
			if keys[pygame.K_e] and not self.timers['seed switch'].active:
				self.timers['seed switch'].activate()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
				self.selected_seed = self.seeds[self.seed_index]

			if keys[pygame.K_f]:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()
					else:
						self.status = 'left_idle'
						self.sleep = True
	def get_status(self):
		
		# 发呆
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# 使用工具
		if self.timers['tool use'].active:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool
	
	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def collision(self, direction):
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: #向右移
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: #向左移
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: #向下移
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # 向上移
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def move(self,dt):#在这里写hitbox连同角色的移动而发生移动

		#归一化,由于向量的矢量和的性质，斜对角速度会变快，故这里要归一化
		if self.direction.magnitude() > 0:#用于检测这个向量的长度是否为0，如果为0就没有方向，所以不能为0
			self.direction = self.direction.normalize()
		
#---------由于后面会有碰撞的过程，故需要将水平与竖直方向分开

		#水平方向移动
		self.pos.x += self.direction.x * self.speed * dt#这个物体的位置位于方向向量乘以自己的速度和时间增量
		self.hitbox.centerx = round(self.pos.x)#变为范围判定，更准
		self.rect.centerx = self.hitbox.centerx#再将矩形中心移到改变后的位置
		#print(f'x坐标为:{self.rect.centerx}')
		self.collision('horizontal')
		#竖直方向移动
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		#print(f'y坐标为:{self.rect.centery}')
		self.collision('vertical')

	def update(self, dt):
		self.input()
		self.get_status()
		self.update_timers()
		self.move(dt)
		self.animate(dt)

class Player_heart(pygame.sprite.Sprite):
	def __init__(self,pos,line_start_tuple:tuple,line_end_tuple:tuple,hp=100,):
		pygame.sprite.Sprite.__init__(self)
		self.hp=hp
		self.image=pygame.image.load('../assets/Image/heart.png')
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()#用向量来表示移动方向
		self.pos = pygame.math.Vector2(self.rect.center)#让人物在移动的同时更新矩形框
		self.speed = 200#玩家速度
		self.line_startx=line_start_tuple[0]
		self.line_endx=line_end_tuple[0]
		self.line_starty=line_start_tuple[1]
		self.line_endy=line_end_tuple[1]
		# self.timers={'game stop': Timer(350,self.game_stop)}
	# def game_stop(self):
	# 	pass
	def update(self):
		key_pressd=pygame.key.get_pressed()
		if key_pressd[pygame.K_d]:
			self.rect.x+=6
		if key_pressd[pygame.K_a]:
			self.rect.x-=6
		if key_pressd[pygame.K_w]:
			self.rect.y-=6
		if key_pressd[pygame.K_s]:
			self.rect.y+=6
		if self.rect.right >=self.line_endx:
			self.rect.right=self.line_endx
		if self.rect.left<=self.line_startx:
			self.rect.left=self.line_startx
		if self.rect.bottom>=SCREEN_HEIGHT:
			self.rect.bottom=SCREEN_HEIGHT
		if self.rect.top<=self.line_starty:
			self.rect.top=self.line_starty

	

class bullet(pygame.sprite.Sprite):
	def __init__(self,line_start_tuple:tuple,line_end_tuple:tuple):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('../assets/Image/B_DOWN_w.png')
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		#出发的坐标
		self.line_startx=line_start_tuple[0]
		self.line_endx=line_end_tuple[0]
		self.line_starty=line_start_tuple[1]
		self.line_endy=line_end_tuple[1]
		self.rect.x=random.randrange(self.line_startx,self.line_endx-self.rect.width)
		self.rect.y=self.line_endy
		self.speedy=random.randrange(2,10)
		self.speedx=random.randrange(-3,3)

	def update(self):
         self.rect.y +=self.speedy
         self.rect.x +=self.speedx
         if self.rect.top > SCREEN_HEIGHT or self.rect.left > self.line_endx or self.rect.right <self.line_startx:
            self.rect.x=random.randrange(self.line_startx,self.line_endx-self.rect.width)
            self.rect.y=self.line_endy
            self.speedy=random.randrange(4,12)
            self.speedx=random.randrange(-4,4)
	


	