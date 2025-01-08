import pygame 
from Setting import *
from Player import Player
from Overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree,Interaction,house,boss,Particle
from pytmx.util_pygame import load_pygame
from soil import SoilLayer
from support import *
from Menu import Menu,stop_menu
from transition import Transition
from sky import Rain, Sky
from add_event import add_event,g_evene_queue 
from random import randint
#这个类用来绘制地图，加载人物，几乎所有的程序都在这里进行
class Level2:
	def __init__(self,player_will):
		self.player_will=player_will
		# get the display surface
		self.display_surface = pygame.display.get_surface()
	
		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()#用于存储哪些组分需要有碰撞判定
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()##用于判断哪些组分碰撞后需要判断有交互
		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition( self.player)

		#天空
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		self.sky = Sky()
		# shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False
		#暂停界面2，只适用于游戏进行中
		self.stop_menu = stop_menu(self.toggle_stop)
		self.stop_active = False
		#作战
		self.battle_active = False

		#音乐
		self.success = pygame.mixer.Sound('../assets/audio/success.wav')
		self.success.set_volume(0.3)


	def setup(self):
		#加载传送门的图片
		self.portal_image=pygame.image.load('../assets/photo/spr_undynehouse_door_0.png').convert_alpha()
		self.portal_image=pygame.transform.scale(self.portal_image, (100,200))
		#传入做好的图片
		tmx_data = load_pygame('../assets/data/map.tmx')
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
		water_frames = import_folder('../assets/graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		# 树部分 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		# 野外植物部分 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		# 碰撞体积部分
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
		
		#boss场景部分
		boss_frames = import_folder('../assets/demon1/react')
		boss((923,340),boss_frames,self.all_sprites)
		
		#玩家部分
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), #设立出生点，避免随机刷新
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop,
					levelint=None)

			if obj.name == 'Bed':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)
			if obj.name == 'Trader':
				Interaction((obj.x,obj.y),(obj.width,obj.height),self.interaction_sprites,obj.name)
		
		
		Generic(
			pos = (0,0),
			surf = pygame.image.load('../assets/graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])#z轴坐标用于分层绘图
		
	def player_add(self,item):#给玩家添加物品,结算奖励
		self.player.item_inventory[item] += 1
		self.success.play()
	def reset(self):
		#植物更新
		self.soil_layer.update_plants()

		#泥土更新
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		if self.raining:
			self.soil_layer.water_all()

		#树上的苹果更新
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		#天空更新
		self.sky.start_color = [255,255,255]
	def toggle_shop(self):
		self.shop_active = not self.shop_active#用于转换，每一次会变成相反数
		# print(self.shop_active)
	def is_win(self):
		
		one_loot_item=0#用来记录有几个物品被抢完了
		one_give_item=0#用来记录送光了多少物品
		#检查商店的物品数量
		for values in self.menu.trader_item_inventory.values():
			if values ==0:
				one_loot_item+=1
		if one_loot_item == 4:#小boss屋部分
			self.portal=house((2065,1741),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2075,1850),(280,146),self.interaction_sprites,'portal')
		for values in self.player.item_inventory.values():
			if values ==0:
				one_give_item+=1
		if one_give_item == 4:
			self.portal=house((2065,1741),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2075,1850),(280,146),self.interaction_sprites,'portal')

		
	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
	
	def toggle_stop(self):
		self.stop_active = not self.stop_active
	def get_player_will(self):
		return self.player_will
	def run(self,dt):

		#绘画逻辑
		self.display_surface.fill('white')
		self.all_sprites.custom_draw(self.player)#更新摄像头
		#更新
		if self.shop_active:
			self.menu.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()

		self.overlay.display()
		# 天气
		self.overlay.display()
		if self.raining and not self.shop_active:
			self.rain.update()
		self.sky.display(dt)

		if self.player.sleep:
			self.transition.play()
		self.is_win()
		if g_evene_queue[-1]==4:
			return 4
		if g_evene_queue[-1]==5:
			return 5
		else:
			return 3

#摄像头的移动，跟随player移动
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
#------------------到此为止---------------