import pygame
import sys
from button import button
from move import move
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
def darw_map():
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('arrests/photo/地图.png')
    # 渲染图片
    window.blit(image1,(0,0))
#------实现动画效果-----------------
    frames_me_forward=[]
    for i in range(1,3):
        frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
        frame=pygame.transform.scale(frame,(50,50))
        frames_me_forward.append(frame)

    frames_me_down=[]
    for i in range(3,5):
        frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
        frame=pygame.transform.scale(frame,(50,50))
        frames_me_down.append(frame)

    frames_me_right=[]
    for i in range(5,7):
        frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
        frame=pygame.transform.scale(frame,(50,50))
        frames_me_right.append(frame)

    frames_me_left=[]
    for i in range(7,9):
        frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
        frame=pygame.transform.scale(frame,(50,50))
        frames_me_left.append(frame)
#--------设置帧率------------------
    clock = pygame.time.Clock()
    index = 0
    pygame.display.update()
    while 1:
    #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        window.fill(WHITE)
        window.blit(frames_me[index],(100,100))
        #-----更新屏幕---------
        pygame.display.update()
        index=(index+1)%len(frames_me)
        clock.tick(FPS)
    pygame.quit()
darw_map()