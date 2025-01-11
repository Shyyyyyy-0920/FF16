import pygame 
from Setting import *
from Player import Player
from Overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree,Interaction,house,boss,Particle
from pytmx.util_pygame import load_pygame
from soil import SoilLayer
from support import *
from Menu import Menu
from transition import Transition
from sky import Rain, Sky
from add_event import g_evene_queue 
from random import randint
from UI import UI
from will import player_will
from chat import ChatBot
from battle import Trader_Battle
#这个类用来绘制地图，加载人物，几乎所有的程序都在这里进行
class Level2:
	def __init__(self):
		
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
		self.menu = Menu(self.player, self.toggle_shop,self.start_talk)
		self.shop_active = False
		#限制次数
		self.use_time =0
		#ui界面
		self.ui=UI()
		#人物的善恶值
		self.player_will=player_will()
		#音乐
		self.success = pygame.mixer.Sound('../assets/audio/success.wav')
		self.success.set_volume(0.3)
		self.rain_sound = pygame.mixer.Sound('../assets/sound/rain.wav')
		self.rain_sound.set_volume(0.2)
		#对话方面
		self.talk_flag=False
		self.ChatBot=ChatBot("trader3")
		##用于接受对话返回到信息
		self.will_change=None
		self.will_change_keep=0
		self.anger_point=None
		self.fight_bool=False
		#与 trader 对战
		self.Trader_Battle=Trader_Battle(self.start_talk)
		#打完trader回来的标志
		self.battle_flag=False

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
		self.boss=boss((923,340),boss_frames,self.all_sprites)
		
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
					toggle_shop = self.toggle_shop
					)

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
		one_mission_item=0#用来记录完成了几个任务
		#检查商店的物品数量
		for values in self.menu.trader_item_inventory.values():
			if values ==0:#抢夺
				one_loot_item+=1
			if values == 6:##完成任务也可以过	
				one_mission_item+=1
		if one_loot_item == 4:#抢光了直接进入战斗
			self.battle_flag=True
		for values in self.player.item_inventory.values():#只要清空背包就行
			if values ==0:
				one_give_item+=1
				values=1
		if one_give_item == 4:
			self.portal=house((2065,1741),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2075,1850),(280,146),self.interaction_sprites,'portal')
		if one_mission_item == 4:
			self.portal=house((2065,1741),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2075,1850),(280,146),self.interaction_sprites,'portal')
			self.player_will.modify_player_will(20)

		
	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
	def talk_with_trader(self):
		self.will_change, self.anger_point, self.fight_bool=self.ChatBot.start(True,self.start_talk)
		if self.fight_bool:
			self.battle_flag=True
			self.will_change_keep=self.will_change
	def toggle_stop(self):
		self.stop_active = not self.stop_active
	def update_will(self):
		self.new_player_will=self.player_will.get_player_will()
	def start_talk(self):
		self.talk_flag=not self.talk_flag
	def check_trader_health(self):
		if self.Trader_Battle.boss_hp<=0 and self.use_time == 0:
			self.player_will.modify_player_will(self.will_change_keep)
			self.boss.kill()
			self.use_time=1
			self.portal=house((2065,1741),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2075,1850),(280,146),self.interaction_sprites,'portal')

	def run(self,dt):
		self.update_will()
		#绘画逻辑
		self.display_surface.fill('white')
		self.all_sprites.custom_draw(self.player)#更新摄像头
		self.ui.show_bar(self.new_player_will,100,self.ui.will_value,PLAYER_WILL_COLOR)
		self.ui.show_bar(100-self.new_player_will,100,self.ui.bad_value,PLAYER_BAD_COLOR)
		#更新
		if self.shop_active:
			if self.talk_flag and not self.battle_flag:
				self.talk_with_trader()
			elif not self.talk_flag and self.battle_flag:
				self.Trader_Battle.run(dt)
			else:
				self.menu.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()
			self.overlay.display()
		self.check_trader_health()
		# 天气
		self.overlay.display()
		if self.raining and not self.shop_active:
			self.rain.update()
			self.rain_sound.play()
		else:
			self.rain_sound.stop()
		self.sky.display(dt)
		
		if self.player.sleep:
			self.transition.play()
		self.is_win()
#--------检查是否跳转页面
		if g_evene_queue[-1]==6:
			self.rain_sound.stop()
			return 6#与最终BOSS对战
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