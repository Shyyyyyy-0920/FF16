import pygame
from Setting import *
from support import *
from Timer import Timer
from add_event import add_event
import random
from math import sin
from chat import ChatBot
#人物类，主要是各个人物属性的创建
class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group,collision_sprites, tree_sprites,interaction,soil_layer,toggle_shop):
		# self.group=group
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
		self.speed = 400#玩家速度

		#碰撞部分的逻辑
		
		self.hitbox = self.rect.copy().inflate((-126,-70))#inflate所做的就是改变矩形的尺寸，同时保持它围绕wall center，传入的元祖为（宽度，高度）
		self.collision_sprites = collision_sprites
        
		# 时钟部分
		self.timers = {
			'tool use': Timer(300,self.use_tool),
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
			'wood':   2,
			'apple':  2,
			'corn':   2,
			'tomato': 2,
		}
		self.money=200
		self.talk_inventory={'talk':0}

		self.seed_inventory = {
		'corn': 5,
		'tomato': 5
		}

		# 有交互的部分
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.toggle_shop = toggle_shop
		self.soil_layer = soil_layer
		
		#音乐
		self.watering = pygame.mixer.Sound('../assets/audio/water.mp3')
		self.watering.set_volume(0.2)
		self.switch_tool = pygame.mixer.Sound('../assets/audio/Menu2.wav')
		self.switch_tool.set_volume(0.8)
		self.switch_seed = pygame.mixer.Sound('../assets/audio/Menu6.wav')
		self.switch_seed.set_volume(0.8)
		self.portal = pygame.mixer.Sound('../assets/audio/Alert.wav')
		self.portal.set_volume(1)
		
	def use_tool(self):
		if self.selected_tool == 'hoe':
			self.soil_layer.get_hit(self.target_pos)
		
		if self.selected_tool == 'axe':
			for tree in self.tree_sprites.sprites():
				if tree.rect.collidepoint(self.target_pos):
					tree.damage()
		
		if self.selected_tool == 'water':
			self.soil_layer.water(self.target_pos)
			self.watering.play()

	def use_seed(self):
		if self.seed_inventory[self.selected_seed] > 0:
			self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
			self.seed_inventory[self.selected_seed] -= 1

	def get_target_pos(self):
		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def import_assets(self):
		#创建一个字典,必须是字典，否则无法让对应的动作显示对应的动画
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[],
						   'right_gun':[],'left_gun':[],'up_gun':[],'down_gun':[]}

		for animation in self.animations.keys():
			full_path = '../assets/graphics/character/' + animation
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
				self.switch_tool.play()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
				self.selected_tool = self.tools[self.tool_index]
			#使用种子
			if keys[pygame.K_LCTRL]:
				self.timers['seed use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0
			# 更换种子
			if keys[pygame.K_e] and not self.timers['seed switch'].active:
				self.timers['seed switch'].activate()
				self.switch_seed.play()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
				self.selected_seed = self.seeds[self.seed_index]

			if keys[pygame.K_f]:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()#这里就是碰撞的判断，如果碰到了就改变商店的状态
					elif collided_interaction_sprite[0].name =='portal':
						global open_stop_time
						open_stop_time=pygame.time.get_ticks()
						self.portal.play()
						add_event(6)
					else:
						self.status = 'left_idle'
						self.sleep = True
					
	def get_status(self):
		
		# 发呆
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# 使用工具的状态
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
		# print(self.pos)
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()
		self.move(dt)
		self.animate(dt)

class Player_battle(pygame.sprite.Sprite):
	def __init__(self,pos,groups,collision_sprites,interaction_sprites,create_attack,destroy_attack,create_magic,levelint,get_talk_info=None,togggle_talk=None):
		super().__init__(groups)
		self.frame_index = 0
		self.image = pygame.image.load('../assets/graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		#图片设置
		self.import_player_assets()
		self.status = 'down'#初始状态

		#移动的初始设置
		self.direction = pygame.math.Vector2()
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		self.obstacle_sprites =collision_sprites
		self.interaction_sprites=interaction_sprites

		#武器
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack

		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True#用来调控武器的switch，避免连续切换
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200


		#魔法攻击
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		#角色的基本属性
		self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
		self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
		self.health = self.stats['health'] * 0.5
		self.energy = self.stats['energy'] * 0.8
		self.exp = 5000
		self.speed = self.stats['speed']

		#造成伤害的时钟
		self.vulnerable = True#受到伤害的标志
		self.hurt_time = None
		self.invulnerability_duration = 500

		#导入音乐
		self.weapon_attack_sound = pygame.mixer.Sound('../assets/audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.4)
		self.switch_weapon = pygame.mixer.Sound('../assets/audio/Menu2.wav')
		self.switch_weapon.set_volume(0.8)
		self.switch_magic = pygame.mixer.Sound('../assets/audio/Menu6.wav')
		self.switch_magic.set_volume(0.8)
		self.portal = pygame.mixer.Sound('../assets/audio/Alert.wav')
		self.portal.set_volume(1)
	

		self.levelint=levelint
		self.togggle_talk=togggle_talk
		#用来返回碰撞怪物的函数
		self.get_talk_info=get_talk_info

	def import_player_assets(self):
		character_path = '../assets/graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			#移动输入
			if keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
	
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
			

			#攻击输入
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
				self.weapon_attack_sound.play()

			# 魔法 input 
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style,strength,cost)

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.switch_weapon.play()
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				self.weapon = list(weapon_data.keys())[self.weapon_index]

			if keys[pygame.K_e] and self.can_switch_magic:
				self.switch_magic.play()
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]
			
			if keys[pygame.K_f]:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction_sprites,False)
				print(9999999)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name =='portal':
						self.portal.play()
						add_event(self.levelint)
					elif collided_interaction_sprite[0].name =='Trader':
						self.togggle_talk()
					elif collided_interaction_sprite[0].name =='Flowey':
						self.get_talk_info("flowey",True)
					elif collided_interaction_sprite[0].name =='Papyrus':
						self.get_talk_info("papyrus",True)
					elif collided_interaction_sprite[0].name =='TEMMIE':
						self.get_talk_info("temmie",True)
					elif collided_interaction_sprite[0].name =='Undyne':
						self.get_talk_info("undyne",True)
					else:
						self.status = 'left_idle'
						self.sleep = True

	def get_status(self):

		# 发呆的状态
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:#攻击的状态
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def cooldowns(self):#用来调控每种武器的攻击间隔
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True

		if not self.vulnerable:#无敌时间
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True
	def wave_value(self):#受到伤害自己会闪，提示玩家自己扣血了
		self.value = sin(pygame.time.get_ticks())
		if self.value >=0:
			return 255
		else:return 0
	def animate(self,dt):
		animation = self.animations[self.status]

		self.frame_index += 4*dt
		if self.frame_index >= len(animation):
			self.frame_index = 0

		#设置图片
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# 闪烁动画
		if not self.vulnerable:
			alpha = self.wave_value()#实现快速闪烁
			self.image.set_alpha(alpha)#设置透明度
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):#获取所有伤害，武器伤害加自己属性的攻击力
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage

	def get_full_magic_damage(self):
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']
		return base_damage + spell_damage

	def get_value_by_index(self,index):#获取现在状态的值
		return list(self.stats.values())[index]

	def get_cost_by_index(self,index):#更新升级消耗的exp
		return list(self.upgrade_cost.values())[index]

	def energy_recovery(self):#用于随时间恢复蓝条
		if self.energy < self.stats['energy']:
			self.energy += 0.005 * self.stats['magic']
		else:
			self.energy = self.stats['energy']
	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def move(self,speed,dt):#在这里写hitbox连同角色的移动而发生移动

		#归一化,由于向量的矢量和的性质，斜对角速度会变快，故这里要归一化
		if self.direction.magnitude() != 0:#用于检测这个向量的长度是否为0，如果为0就没有方向，所以不能为0
			self.direction = self.direction.normalize()*1.3
		
#---------由于后面会有碰撞的过程，故需要将水平与竖直方向分开

		#水平方向移动
		self.hitbox.x += self.direction.x * (speed-3) * (dt*100)#这个物体的位置位于方向向量乘以自己的速度和时间增量
		self.collision('horizontal')
		#竖直方向移动
		self.hitbox.y += self.direction.y * (speed-3) * (dt*100)
		self.collision('vertical')
		self.rect.center = self.hitbox.center
	def update(self,dt):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate(dt)
		self.move(self.stats['speed'],dt)
		self.energy_recovery()
#人物魔法值的消耗
class MagicPlayer:
	def __init__(self,animation_player):
		self.animation_player = animation_player
		self.sounds = {
		'heal': pygame.mixer.Sound('../assets/audio/heal.wav'),
		'flame':pygame.mixer.Sound('../assets/audio/Fire.wav')
		}
#两个魔法效果
	def heal(self,player,strength,cost,groups):#恢复效果
		if player.energy >= cost:
			self.sounds['heal'].play()
			player.health += strength
			player.energy -= cost
			if player.health >= player.stats['health']:
				player.health = player.stats['health']
			self.animation_player.create_particles('aura',player.rect.center,groups)
			self.animation_player.create_particles('heal',player.rect.center,groups)

	def flame(self,player,cost,groups):#释放火焰刀方向
		if player.energy >= cost:
			player.energy -= cost
			self.sounds['flame'].play()

			if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
			elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
			elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
			else: direction = pygame.math.Vector2(0,1)

			for i in range(1,6):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILE_SIZE
					x = player.rect.centerx + offset_x + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)#加几个随机数，更加真实的火焰攻击
					y = player.rect.centery + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILE_SIZE
					x = player.rect.centerx + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
					y = player.rect.centery + offset_y + random.randint(-TILE_SIZE // 3, TILE_SIZE // 3)
					self.animation_player.create_particles('flame',(x,y),groups)

class Player_heart(Player):
	def __init__(self, pos, group, collision_sprites,interaction,toggle_stop):
		super().__init__(
			pos = pos, 
			group = group, 
			collision_sprites = collision_sprites,
			interaction = interaction,
			tree_sprites = None,
			soil_layer = None,
			toggle_shop = toggle_stop)
		self.image=pygame.image.load('../assets/Image/heart/0.png')
		self.rect=self.image.get_rect(center = pos)
		self.hp=100
		self.vulnerable = True#受到伤害的标志
		self.stop_open=False#开启暂停页面的标志
		
		self.invulnerability_duration = 500
		self.hurt_time = None
		#获取遮罩，用于完美像素判断碰撞
		self.mask=pygame.mask.from_surface(self.image)
	def animate(self,dt):
		self.frames=import_folder('../assets/Image/heart')
		self.frame_index += 15*dt#帧速率，但是会返回一个浮点数，下面这个记得转换
		#由于每个动作组都有有限的数量,要让动画只会循环这个
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
	def input(self):
		keys = pygame.key.get_pressed()
		#方向
		if keys[pygame.K_w]:
			self.direction.y = -1#这些都表示某个方向向量
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		if keys[pygame.K_f] and self.stop_open:
			self.toggle_shop()
	def is_defeat(self):
		if self.hp<=0:
			self.kill()
	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.vulnerable:#无敌时间
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True
		if not self.stop_open:
			if current_time - open_stop_time >=500:
				self.stop_open= True
	def move(self,dt):#在这里写hitbox连同角色的移动而发生移动

		#归一化,由于向量的矢量和的性质，斜对角速度会变快，故这里要归一化
		if self.direction.magnitude() > 0:#用于检测这个向量的长度是否为0，如果为0就没有方向，所以不能为0
			self.direction = self.direction.normalize()
		
#---------由于后面会有碰撞的过程，故需要将水平与竖直方向分开
		#水平方向移动
		self.pos.x += self.direction.x * self.speed * dt#这个物体的位置位于方向向量乘以自己的速度和时间增量
		self.hitbox.centerx = round(self.pos.x)#变为范围判定，更准
		self.rect.centerx = self.hitbox.centerx#再将矩形中心移到改变后的位置
		self.collision('horizontal')
		if self.rect.right>=700:
			self.rect.right=700
		elif self.rect.left<=100:
			self.rect.left=100
		#竖直方向移动
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		#print(f'y坐标为:{self.rect.centery}')
		self.collision('vertical')
		if self.rect.bottom>=530:
			self.rect.bottom=530
		elif self.rect.top<=200:
			self.rect.top=200
	def update(self,dt):
		self.input()
		self.cooldowns()
		self.move(dt)
		self.animate(dt)
		self.is_defeat()
#----------------到此为止-------------	
