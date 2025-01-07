from pygame.math import Vector2
import pygame
FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 64
#背景的图片的大下获取
background=pygame.image.load('../assets/graphics/world/ground.png')
BACKGROUND_WIDTH=background.get_width()
BACKGROUND_HEIGHT=background.get_height()
# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../assets/font/DTM-Mono.otf'
UI_FONT_SIZE = 18
# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}

weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../assets/graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../assets/graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../assets/graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../assets/graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../assets/graphics/weapons/sai/full.png'}}
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'../assets/graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../assets/graphics/particles/heal/heal.png'}}
# enemy
monster_data = {
	'Papyrus': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'Undyne': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../assets/audio/attack/claw.wav','speed': 2.5, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'TEMMIE': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../assets/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'Flowey': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

#----------到此为止---------------------