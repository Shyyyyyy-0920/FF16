from pygame.math import Vector2
import pygame
FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
class WindowSettings:
    name='UnderTruth'
    width=800
    height=720
    outdoorScale=1.5

class PlayerSettings:
    playerSpeed = 5
    playerWidth = 60
    playerHeigth = 55

class SceneSettings:
    tileXnum = 48
    tileYnum = 27
    tileWidth = tileHeight = 40

class GamePath:
    gamer = [[r".\assets\graphics\character\down\0.png",r'.\assets\graphics\character\down\1.png',r'.\assets\graphics\character\down\2.png',r'.\assets\graphics\character\down\3.png'],
              [r'.\assets\graphics\character\left\0.png',r'.\assets\graphics\character\left\1.png',r'.\assets\graphics\character\left\2.png',r'.\assets\graphics\character\left\3.png'],
              [r'.\assets\graphics\character\right\0.png',r'.\assets\graphics\character\right\1.png',r'.\assets\graphics\character\right\2.png',r'.\assets\graphics\character\right\3.png'],
              [r'.\assets\graphics\character\up\0.png',r'.\assets\graphics\character\up\1.png',r'.\assets\graphics\character\up\2.png',r'.\assets\graphics\character\up\3.png']]

    groundTileds = []

    tree = [r'.\arrests\graphics\objects\tree_small.png',
            r'.\arrests\graphics\objects\tress_medium.png']
    mapobj=r'.\assets\graphics\world\ground.png'
class GameState:
    MAIN_MENU=1
    GAME_LOADING = 2
    GAME_OVER=3
    GAME_WIN=4
    GAME_PAUSE = 5
    GAME_PLAY_WILD=6



# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 64
#背景的图片的大下获取
background=pygame.image.load('../graphics/world/ground.png')
BACKGROUND_WIDTH=background.get_width()
BACKGROUND_HEIGHT=background.get_height()


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
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}