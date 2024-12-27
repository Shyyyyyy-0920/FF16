import pygame 
from Setting import *
from Player import Player
from Overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree,Interaction,house,boss
from pytmx.util_pygame import load_pygame
from support import *
from Menu import Menu
from transition import Transition
from battle import Battle
from sky import Rain, Sky
from random import randint

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()#用于存储哪些组分需要有碰撞判定
		self.interaction_sprites = pygame.sprite.Group()

		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition( self.player)

		#天空
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		# self.soil_layer.raining = self.raining
		self.sky = Sky()
		# shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False
		#战斗
		self.battle=Battle((0,200),(800,200))
		self.battle_active = False


	def setup(self):
		#传入做好的图片
		tmx_data = load_pygame('../data/map.tmx')
#----------------
		# 房子部分 
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)

		# 围栏部分
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		# 水部分
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		# 树部分 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites], obj.name)

		# 野外植物部分 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		# 碰撞体积部分
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
		
		#boss场景部分
		boss_frames = import_folder('../assets/人物/demon1/react')
		boss((923,340),boss_frames,self.all_sprites)

		#小屋部分
		house((2065,1741),pygame.image.load('../assets/Image/三角屋(60x73).png').convert_alpha(),[self.all_sprites, self.collision_sprites])

		#玩家部分
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), #设立出生点，避免随机刷新
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					# tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					# soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop)

			if obj.name == 'Bed':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)
			if obj.name == 'Trader':
				Interaction((obj.x,obj.y),(obj.width,obj.height),self.interaction_sprites,obj.name)
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])#z轴坐标用于分层绘图
		
		
	def player_add(self,item):#给玩家添加物品

		self.player.item_inventory[item] += 1

	def toggle_shop(self):
		self.shop_active = not self.shop_active#用于转换，每一次会变成相反数
#--------物品收集----------------------
	# def plant_collision(self):
	# 	if self.soil_layer.plant_sprites:
	# 		for plant in self.soil_layer.plant_sprites.sprites():
	# 			if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
	# 				self.player_add(plant.plant_type)
	# 				plant.kill()
	# 				self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	# def goto(self):
	# 	pass
	def run(self,dt):
		#绘画逻辑
		self.display_surface.fill('white')
		self.all_sprites.custom_draw(self.player)
		#更新
		#这里是如果开始商店里那么其他东西停止更新，感觉可以用于做暂停界面
		if self.shop_active:
			self.menu.update()
		elif self.battle_active:
			self.battle.update(dt)
		else:
			self.all_sprites.update(dt*2)
        #这里或许可以加上天气的代码
		self.overlay.display()

		if self.player.sleep:
			self.transition.play()

class CameraGroup(pygame.sprite.Group):#摄像头的工作
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2#这里两行的逻辑保证了玩家在画面中央
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:#这里判断z轴的涂层
					offset_rect = sprite.rect.copy()#，并且移动相机
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)