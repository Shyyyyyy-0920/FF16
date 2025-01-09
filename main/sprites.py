import pygame
from Setting import *
from support import *
from random import randint,choice,randrange
from math import sin
#各类地图中npc，景色的组分创建，加上各自的碰撞体积
class Generic(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z=z#z轴坐标，用于分层
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
class sans(Water):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups)
class WildFlower(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)
class Particle(Generic):
	def __init__(self, pos, surf, groups, z, duration = 200):
		super().__init__(pos, surf, groups, z)
		self.start_time = pygame.time.get_ticks()
		self.duration = duration

		mask_surf = pygame.mask.from_surface(self.image)
		new_surf = mask_surf.to_surface()
		new_surf.set_colorkey((0,0,0))
		self.image = new_surf

	def update(self,dt):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time > self.duration:
			self.kill()
class Tree(Generic):
	def __init__(self, pos, surf, groups, name,player_add):
		super().__init__(pos, surf, groups)
		#树的一些设置
		self.health = 5
		self.alive = True
		stump_path = f'../assets/graphics/stumps/{"small" if name == "Small" else "large"}.png'
		self.stump_surf = pygame.image.load(stump_path).convert_alpha()

		#苹果掉落
		self.apple_surf = pygame.image.load('../assets/graphics/fruit/apple.png')
		self.apple_pos = APPLE_POS[name]
		self.apple_sprites = pygame.sprite.Group()
		self.create_fruit()

		self.player_add = player_add
		#声音
		self.axe_sound = pygame.mixer.Sound('../assets/audio/axe.mp3')

	def damage(self):
		
		#破坏树，树都生命值减1
		self.health -= 1

		self.axe_sound.play()
		#掉落苹果
		if len(self.apple_sprites.sprites()) > 0:
			random_apple = choice(self.apple_sprites.sprites())
			Particle(
				pos = random_apple.rect.topleft,
				surf = random_apple.image, 
				groups = self.groups()[0], 
				z = LAYERS['fruit'])
			self.player_add('apple')
			random_apple.kill()

	def check_death(self):
		if self.health <= 0:
			Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruit'], 300)
			self.image = self.stump_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
			self.alive = False
			self.player_add('wood')

	def update(self,dt):
		if self.alive:
			self.check_death()

	def create_fruit(self):
		for pos in self.apple_pos:
			if randint(0,10) < 2:
				x = pos[0] + self.rect.left
				y = pos[1] + self.rect.top
				Generic(
					pos = (x,y), 
					surf = self.apple_surf, 
					groups = [self.apple_sprites,self.groups()[0]],
					z = LAYERS['fruit'])

class house(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf,groups)
		# self.image=pygame.transform.scale(self.image,(200,300))
		self.pos=pos
		self.hitbox = self.rect.copy().inflate(-20,-self.rect.height*0.6)

class boss(Generic):
	def __init__(self, pos, frames, groups):
		#动画设置
		self.frames = frames
		self.frame_index = 0
	# 群组设置
		super().__init__(
				pos = pos, 
				surf = self.frames[self.frame_index], 
				groups = groups) 
		self.z=LAYERS['main']

	def animate(self,dt):
		self.frame_index += 5 * dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
		self.image=pygame.transform.scale(self.image,(90,120))

	def update(self,dt):
		self.animate(dt)
class block(Generic):#用来限制人物行动范围
	def __init__(self, pos, surf, groups, z=LAYERS['main']):
		super().__init__(pos, surf, groups, z)
class attack(Generic):#sans的一些攻击
	def __init__(self, pos,type, groups,speed,vector1):#说明，vector1是方向向量，用来表示这个攻击物的移动方向
		#动画设置
		self.frame_index = 0
		self.frames=pygame.image.load( '../assets/graphics/monsters/sans/Attacks/battle_1/spr_gasterblaster_0.png')
		# 群组设置
		super().__init__(
				pos = pos, 
				surf =self.frames, 
				groups = groups) 
		self.hitbox = self.rect.inflate(0,-10)
		self.type=type
		self.speed=speed
		self.direction=vector1
	def animate(self,dt):
		if self.type == 'battle_1' :
			self.frames = import_folder('../assets/graphics/monsters/sans/Attacks/battle_1')
			self.frame_index += 5 * dt
			if self.frame_index >= len(self.frames):
				self.frame_index = 0
				self.image = self.frames[int(self.frame_index)]
		else:
			pass
	def move(self,dt):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		self.rect.x += self.direction.x *self.speed*dt
		self.rect.y += self.direction.y *self.speed*dt
		if self.rect.y >=600:
			self.rect.y=200
		if self.rect.x>=800:
			self.rect.x=randint(0,800)
		#self.rect.center = self.hitbox.center
	def update(self,dt):
		self.move(dt)
		self.animate(dt)

class Enemy(pygame.sprite.Sprite):#所有的怪物类
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):

		#普通设置
		super().__init__(groups)
		self.frame_index = 0
		self.sprite_type = 'enemy'

		#图片设置
		self.import_graphics(monster_name)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]

		#移动
		self.direction = pygame.math.Vector2()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		#每个怪的属性
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

		#与玩家之间的交互
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.add_exp = add_exp

		#无敌时间，防止直接死亡
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		#声音设置
		self.death_sound = pygame.mixer.Sound('../assets/audio/death.wav')
		self.hit_sound = pygame.mixer.Sound('../assets//audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0.6)
		self.hit_sound.set_volume(0.6)
		self.attack_sound.set_volume(0.6)

	def import_graphics(self,name):
		self.animations = {'idle':[],'move':[],'attack':[]}
		main_path = f'../assets/graphics/monsters/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self,player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()
	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: 
			return 255
		else: 
			return 0
	def animate(self,dt):
		animation = self.animations[self.status]
		
		self.frame_index += 4*dt
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self,player,attack_type):
		if self.vulnerable:
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)
			self.add_exp(self.exp)
			self.death_sound.play()
	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance
	def move(self,speed,dt):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * (speed-1)*(dt*95)
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * (speed-1)*(95*dt)
		self.collision('vertical')
		self.rect.center = self.hitbox.center
	def collision(self,direction):
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
	def update(self,dt):
		self.hit_reaction()
		self.move(self.speed,dt)
		self.animate(dt)
		self.cooldowns()
		self.check_death()

	def enemy_update(self,player):
		self.get_status(player)
		self.actions(player)
					
class collision_rect(Generic):# 障碍物的类、
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy().inflate(0,0)
class Tile(Generic):
	def __init__(self,pos,surface,groups,sprite_type):
		super().__init__(pos,surface,groups)
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILE_SIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
	
class bullet(pygame.sprite.Sprite):
	def __init__(self,line_start_tuple:tuple,line_end_tuple:tuple):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load('../assets/Image/B_DOWN_w.png')
		self.rect = self.image.get_rect()
		#出发的坐标
		self.line_startx=line_start_tuple[0]
		self.line_endx=line_end_tuple[0]
		self.line_starty=line_start_tuple[1]
		self.line_endy=line_end_tuple[1]
		self.rect.x=randrange(self.line_startx,self.line_endx-self.rect.width)
		self.rect.y=self.line_endy
		self.speedy=randrange(3,12)
		self.speedx=randrange(-4,4)
		#获取遮罩，用于完美像素判断碰撞
		self.mask=pygame.mask.from_surface(self.image)

	def update(self,dt):
         self.rect.y +=self.speedy*dt*70
         self.rect.x +=self.speedx*dt*70
         if self.rect.top > SCREEN_HEIGHT or self.rect.left > self.line_endx or self.rect.right <self.line_startx:
            self.rect.x=randrange(self.line_startx,self.line_endx-self.rect.width)
            self.rect.y=self.line_endy
            self.speedy=randrange(4,12)
            self.speedx=randrange(-4,4)	

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		#图片的导入
		full_path = f'../assets/graphics/weapons/{player.weapon}/{direction}.png'
		self.image = pygame.image.load(full_path).convert_alpha()
		
		#图片生成的位置
		if direction == 'right':
			self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,16))
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,16))
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,-5))
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,5))
	
		
