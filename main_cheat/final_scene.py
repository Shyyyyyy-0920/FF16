import pygame,sys
from Player import Chara,Toriel
from sprites import house,Interaction
class final_scene_True:
    def __init__(self):
        self.use_time=0
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()##用于判断哪些组分碰撞后需要判断有交互
        self.activate=False
        self.over_image=pygame.image.load('../assets/photo/over0.png').convert_alpha()
    def set_up(self):
             #加载传送门的图片
        self.portal_image=pygame.image.load('../assets/photo/spr_undynehouse_door_0.png').convert_alpha()
        self.portal_image=pygame.transform.scale(self.portal_image, (100,200))
        self.portal=house((400,200),self.portal_image,[self.all_sprites, self.collision_sprites])
        self.Toriel=Toriel((100,400),self.all_sprites,self.collision_sprites,self.interaction_sprites)
        Interaction((400,300),(128,256),self.interaction_sprites,'portal')
    def run(self,dt):
        self.display_surface.fill('black')
        if self.use_time == 0:
            self.start_time=pygame.time.get_ticks()
            self.set_up()
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.quit()
            pygame.mixer.init()
            pygame.mixer.music.load('../assets/sound/bgm2.ogg')
            pygame.mixer.music.set_volume(0.6)              
            pygame.mixer.music.play(loops=-1)
            self.use_time=1
        self.activate = self.Toriel.input()
        if self.activate:
            while 1 :
                self.display_surface.fill('black')
                self.display_surface.blit(self.over_image,(0,0))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        self.now_time=pygame.time.get_ticks()
        self.interval=self.now_time-self.start_time
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        return 7
class final_scene_False:
    def __init__(self):
        self.use_time=0
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()##用于判断哪些组分碰撞后需要判断有交互
        self.activate=False
        self.over_image=pygame.image.load('../assets/photo/over1.png').convert_alpha()
    def set_up(self):
        #加载传送门的图片
        self.portal_image=pygame.image.load('../assets/photo/spr_undynehouse_door_0.png').convert_alpha()
        self.portal_image=pygame.transform.scale(self.portal_image, (100,200))
        self.portal=house((400,200),self.portal_image,[self.all_sprites, self.collision_sprites])
        self.Chara=Chara((100,400),self.all_sprites,self.collision_sprites,self.interaction_sprites)
        Interaction((400,300),(128,256),self.interaction_sprites,'portal')
    def run(self,dt):
        self.display_surface.fill('black')
        if self.use_time == 0:
            self.start_time=pygame.time.get_ticks()
            self.use_time=1
            self.set_up()
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.quit()
            pygame.mixer.init()
            pygame.mixer.music.load('../assets/sound/bgm2.ogg')
            pygame.mixer.music.set_volume(0.6)              
            pygame.mixer.music.play(loops=-1)
        self.activate = self.Chara.input()
        if self.activate:
            while 1 :
                self.display_surface.fill('black')
                self.display_surface.blit(self.over_image,(0,0))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        self.now_time=pygame.time.get_ticks()
        self.interval=self.now_time-self.start_time
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        return 8
#---------到此为止------------