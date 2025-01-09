import pygame
from Setting import *
from Level2 import CameraGroup
from sprites import Generic,collision_rect,Interaction,boss
from Player import Player_battle
from add_event import g_evene_queue,add_event
from support import import_folder
class born_place:
    def __init__(self,player_will):
        
        self.display_surface= pygame.display.get_surface()
        self.player_will=player_will
        self.all_sprites = CameraGroup()
        self.z=LAYERS['ground']
        self.collision_sprites = pygame.sprite.Group()#用于存储哪些组分需要有碰撞判定
        self.interaction_sprites = pygame.sprite.Group()##用于判断哪些组分碰撞后需要判断有交互
        self.set_up()

    def set_up(self):
        stone_image=pygame.image.load('../assets/air/1.png')
        collision_rect((20,-40),stone_image,self.collision_sprites)
        collision_rect((84,-40),stone_image,self.collision_sprites)
        for i in range(18):
            if i <=5:
                collision_rect((170+64*i,420),stone_image,self.collision_sprites)
                collision_rect((170,64*i),stone_image,self.collision_sprites)
            collision_rect((665+64*i,420),stone_image,self.collision_sprites)
            collision_rect((10,-40+64*i),stone_image,self.collision_sprites)
            collision_rect((10+64*i,794),stone_image,self.collision_sprites)
            collision_rect((1100,420+64*i),stone_image,self.collision_sprites)

        self.player = Player_battle(
            pos=(110,18),
            groups=self.all_sprites,
            collision_sprites=self.collision_sprites,
            interaction_sprites=self.interaction_sprites,
            create_attack=None,
            destroy_attack=None,
            create_magic=None,
            levelint=2
        )
        self.player.z=LAYERS['main']
        #传送门部分的空气墙 
        collision_rect((600,380),stone_image,self.collision_sprites)
        Interaction((605,420),(80,50),self.interaction_sprites,'portal')
        self.image=pygame.image.load('../assets/photo/night_ground.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (SCREEN_WIDTH+400,SCREEN_HEIGHT+400))
        #boss场景部分
        boss_frames = import_folder('../assets/demon1/react')
        boss((1000,547),boss_frames,self.all_sprites)
        Interaction((1110,620),(80,50),self.interaction_sprites,'Trader')

        Generic(
			pos = (0,0),
			surf = self.image,
			groups = self.all_sprites,
			z = LAYERS['ground'])#z轴坐标用于分层绘图
    def get_player_will(self):
        return self.player_will
    def cannot_move(self):#(606,512),(141.809,505.98),133.429
        if self.player.rect.centerx<=93.0294:
            self.player.rect.centerx=93.0294
        
        if self.player.rect.centery>=773:
            self.player.rect.centery=773
        if self.player.rect.centerx>=1081.36:
            self.player.rect.centerx=1081.36
    def reset(self):
        # 清空所有精灵组
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.interaction_sprites.empty()
        self.set_up()
    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)#更新摄像头
        self.all_sprites.update(dt*2)
        #print(self.player.rect)
        if g_evene_queue[-1] ==1:
            return 1
        else:
            self.reset()
            return 2
        
#-------------到此为止--------------    