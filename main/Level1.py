import pygame 
from Setting import *
from Level2 import CameraGroup
from support import *
from UI import UI
from Menu import Upgrade
from particles import AnimationPlayer
from Player import MagicPlayer,Player_battle
from sprites import Tile,Weapon,Enemy,house,Interaction
from add_event import g_evene_queue
from random import choice, randint
from add_event import add_event
from display_will import will
class Level1:
	def __init__(self,player_will):
		#人物善恶值
		self.player_will=player_will
		# 获取屏幕表面
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False
		
        # sprite group setup
		self.all_sprites = YSortCameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.all_moster_sprites=pygame.sprite.Group()#用于记录怪物是否全部交谈过或者死亡
		self.interaction_sprites = pygame.sprite.Group()##用于判断哪些组分碰撞后需要判断有交互
		
        #攻击组分
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		
        #初始化
		self.set_up()
		self.init_num=len(self.all_moster_sprites)
        #人物ui界面
		self.ui = UI(self.player_will)
		self.upgrade = Upgrade(self.player)#升级的场景
		
        #粒子效果
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)
		
		
	def set_up(self):
		#加载传送门的图片
		self.portal_image=pygame.image.load('../assets/photo/spr_undynehouse_door_0.png').convert_alpha()
		self.portal_image=pygame.transform.scale(self.portal_image, (100,200))
		layouts = {
			'boundary': import_csv_layout('../assets/map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../assets/map/map_Grass.csv'),
			'object': import_csv_layout('../assets/map/map_Objects.csv'),
			'entities': import_csv_layout('../assets/map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('../assets/graphics/Grass'),
			'objects': import_folder('../assets/graphics/objects')
		}
		#绘制地图
		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILE_SIZE
						y = row_index * TILE_SIZE
						if style == 'boundary':
							Tile((x,y), pygame.Surface((TILE_SIZE,TILE_SIZE)),[self.collision_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								random_grass_image,
								[self.all_sprites,self.collision_sprites,self.attackable_sprites],
								'grass'
								)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),surf,[self.all_sprites,self.collision_sprites],'object')

						if style == 'entities':
							if col == '394':
								self.player = Player_battle(
									(x,y),
									[self.all_sprites],
									self.collision_sprites,
									self.interaction_sprites,
									self.create_attack,
									self.destroy_attack,
									self.create_magic,
									3)
							else:
								if col == '390': monster_name = 'Flowey'
								elif col == '391': monster_name = 'TEMMIE'
								elif col == '392': monster_name ='Undyne'
								else: monster_name = 'Papyrus'
								Enemy(
									monster_name,
									(x,y),
									[self.all_sprites,self.attackable_sprites,self.all_moster_sprites],
									self.collision_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp
									)
								
	def create_attack(self):
		self.current_attack = Weapon(self.player,[self.all_sprites,self.attack_sprites])
	def create_magic(self,style,strength,cost):
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.all_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.all_sprites,self.attack_sprites])
	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None
	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos - offset,[self.all_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)
	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.all_sprites])
	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.all_sprites)
	def add_exp(self,amount):
		self.player.exp += amount
	def toggle_menu(self):
		self.game_paused = not self.game_paused 
	def check_monster_death_num(self):
		if self.init_num>len(self.all_moster_sprites):
			self.player_will-=self.init_num-len(self.all_moster_sprites)
			self.init_num=len(self.all_moster_sprites)
	def is_win(self):
		number_of_monster = len(self.all_moster_sprites)
		if number_of_monster == 34:
			self.portal=house((2153,956),self.portal_image,[self.all_sprites, self.collision_sprites])
			Interaction((2153,956),(280,146),self.interaction_sprites,'portal')
	def get_player_will(self):
		self.check_monster_death_num()
		return self.player_will

	def run(self,dt):
		self.display_surface.fill(WATER_COLOR)
		self.all_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		#print(self.player.rect)
		if self.game_paused:
			self.upgrade.display()
		else:
			self.all_sprites.update(dt)
			self.all_sprites.enemy_update(self.player)
			self.player_attack_logic()
		self.is_win()
		if g_evene_queue[-1]==3:

			return 3
		else:

			return 2
class YSortCameraGroup(CameraGroup):
	def __init__(self):
		super().__init__()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		# creating the floor
		self.floor_surf = pygame.image.load('../assets/graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
	def custom_draw(self,player):

		# 画镜头
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		#画地面
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# 遍历组分
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
#--画怪物---------
	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
