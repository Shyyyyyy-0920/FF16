import pygame
import sys
import random
from button import button
FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
clock=pygame.time.Clock()
pygame.init()
window_lenth=800#窗口初始长度
window_height=600#窗口初始宽度
#创建游戏窗口
window=pygame.display.set_mode((window_lenth,window_height))
#C设置游戏标题
pygame.display.set_caption('真相之下')
 #设置游戏背景颜色
window.fill(BLACK)
line_start_lst=[0,200]
line_end_lst=[800,200]
pygame.display.flip()
class my_heart(pygame.sprite.Sprite):
    HP=100
    def __init__(self,line_start_lst,line_end_lst):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('arrests/Image/heart.png')
        
        self.rect=self.image.get_rect()
        self.rect.center = (window_lenth/2,window_height/2)
        self.rect.bottom= window_height-3
        self.line_start_lst=line_start_lst
        self.line_end_lst=line_end_lst
    def update(self):
        key_pressd=pygame.key.get_pressed()
        if key_pressd[pygame.K_d]:
            self.rect.x+=6
        elif key_pressd[pygame.K_a]:
            self.rect.x-=6
        elif key_pressd[pygame.K_w]:
            self.rect.y-=6
        elif key_pressd[pygame.K_s]:
            self.rect.y+=6
        if self.rect.right >=self.line_end_lst[0]:
            self.rect.right=self.line_end_lst[0]
        if self.rect.left<=self.line_start_lst[0]:
            self.rect.left=self.line_start_lst[0]
        if self.rect.bottom>=window_height:
            self.rect.bottom=window_height
        if self.rect.top<=self.line_start_lst[1]:
            self.rect.top=self.line_start_lst[1]

class bullet(pygame.sprite.Sprite):
    def __init__(self,line_start_lst,line_end_lst):
        self.line_start_lst=line_start_lst
        self.line_end_lst=line_end_lst
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('arrests/Image/B_DOWN_w.png')
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(self.line_start_lst[0],self.line_end_lst[0]-self.rect.width)
        self.rect.y=self.line_end_lst[1]
        self.speedy=random.randrange(2,10)
        self.speedx=random.randrange(-3,3)
    def update(self):
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx
        if self.rect.top > window_height or self.rect.left > self.line_end_lst[0]or self.rect.right <self.line_start_lst[0]:
            self.rect.x=random.randrange(self.line_start_lst[0],self.line_end_lst[0]-self.rect.width)
            self.rect.y=self.line_end_lst[1]
            self.speedy=random.randrange(4,12)
            self.speedx=random.randrange(-4,4)
def battle(line_start_lst,line_end_lst):
    line_start=tuple(line_start_lst)
    line_end=tuple(line_end_lst)
    myhp=my_heart.HP#用于记录战斗时的血量
    all_sprites=pygame.sprite.Group()
    bullets=pygame.sprite.Group()
    player = my_heart(line_start_lst,line_end_lst)
    all_sprites.add(player)
    for i in range(8):
        b=bullet(line_start_lst,line_end_lst)
        all_sprites.add(b)
        bullets.add(b)

    while 1:
        clock.tick(FPS)
        #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        all_sprites.update()
        #判断是否发生碰撞
        hits=pygame.sprite.spritecollide(player,bullets,False)
        if hits:
            myhp=myhp-1
            if myhp<=0:
                return 3
        #用于显示血量 
        title_HP=str(myhp)
        window.fill(BLACK)
        show_hp=button(0,0,0,30,30,660,550,title_HP,30,255,255,255)
        show_hp.draw_button(window)
        
        
        boss_image=pygame.image.load('arrests/人物/demon/idle1.png')
        window.blit(boss_image,(line_end_lst[0]/2,line_start_lst[1]-200))
        all_sprites.draw(window)
        pygame.draw.line(window,(255,255,255),line_start,line_end)
        pygame.display.update()
    pygame.quit()