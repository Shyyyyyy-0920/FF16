import pygame
import sys
from Player import Player_heart,bullet
from Setting import *
from Menu import defeat_menu
from button import button
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.flip()
class Battle:
    def __init__(self,line_start_tuple,line_end_tuple):
        self.line_start_tuple=line_start_tuple
        self.line_end_tuple=line_end_tuple
    def battle(self,dt):
        all_sprites=pygame.sprite.Group()
        bullets=pygame.sprite.Group()#单独创建一个子弹组，用于不断更新子弹数目保持不变
        player_heart=Player_heart((400,300),self.line_start_tuple,self.line_end_tuple)
        myhp=player_heart.hp#用于记录战斗时的血量
        #获取开始时间
        start_ticks=pygame.time.get_ticks()
        all_sprites.add(player_heart)
        for i in range(10):
            b=bullet((0,200),(800,200))
            all_sprites.add(b)
            bullets.add(b)
            boss_hp=100
        while 1:
            dt#帧率控制
            #检测事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            all_sprites.update()
             #判断是否发生碰撞
            hits=pygame.sprite.spritecollide(player_heart,bullets,False)
            if hits:
                myhp=myhp-1
                if myhp<=0:
                    defeat_menu(window,self.battle)
       
            #用于显示血量 
            title_HP=myhp
            title_time=int((pygame.time.get_ticks()-start_ticks)/1000)
        
            window.fill(BLACK)
            show_hp=button(0,0,0,30,30,660,550,f'HP: {title_HP}',30,255,255,255)
            show_time=button(0,0,0,30,30,150,550,f'TIME: {title_time}',30,255,255,255)
            show_hp.draw_button(window)
            show_time.draw_button(window)
        
            boss_image=pygame.image.load('../assets/人物/demon/idle1.png')
            show_boss_hp=button(0,0,0,30,30,660,100,f'BOSSHP: {boss_hp}',30,255,255,255)
            show_boss_hp.draw_button(window)
            window.blit(boss_image,(self.line_end_tuple[0]/2,self.line_start_tuple[1]-200))
            all_sprites.draw(window)
            if (title_time/10)%10==2:
                boss_hp=80
                for i in range(5):
                    all_sprites.add(b)
                    bullets.add(b)
                pygame.draw.line(window,(255,255,255),(self.line_start_tuple[0]+100,self.line_start_tuple[1]),(self.line_start_tuple[0]+100,600))
                pygame.draw.line(window,(255,255,255),(self.line_end_tuple[0]-100,self.line_end_tuple[1]),(self.line_end_tuple[0]-100,600))
  
            pygame.draw.line(window,(255,255,255),self.line_start_tuple,self.line_end_tuple)
        
            pygame.display.update()
    def update(self,dt):
        self.battle(self.line_start_tuple,self.line_end_tuple,dt)


