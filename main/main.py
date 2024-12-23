import pygame
import sys
from EntityLike import EntityLike
# from Event import Event
# from Listener import Listener
# from Player import Player
# from SceneLike import SceneLike
# from Tile import Tile
# from Wall import Wall

g_evene_queue=[]#事件队列，用于读取当前处于什么事件
def add_event(event):  # 向事件队列中添加事件
    g_evene_queue.append(event)



DRAW = 1#第一个事件，画图
STEP = 2#第二个事件，步骤？？？
REQUEST_MOVE = 3#第三个事件，移动的请求
CAN_MOVE = 4#第四个事件，允许移动

FPS=60#避免电脑差异，锁定帧率
BLACK=(0,0,0)#设置常量，表示黑色
WHITE=(255,255,255)#设置常量，表示黑色

clock=pygame.time.Clock()

pygame.init()#初始化
window_lenth=800#窗口初始长度
window_height=600#窗口初始宽度

#创建游戏窗口
window=pygame.display.set_mode((window_lenth,window_height))
#C设置游戏标题
pygame.display.set_caption('真相之下')
 #设置游戏背景颜色
window.fill(WHITE)

pygame.display.flip()#第一次刷新
flag=0#用于跳转界面
while 1 :
    clock.tick(FPS)
        #检测事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        add_event(event)#将每次操作存入事件中
#----------------这里写读取事件以及产生的影响------
        Menu=EntityLike('arrests/photo/background_menu.png',(0,0,window_lenth,window_height))
        Menu.draw([1,10])

#-----------------------------------------------
        #这里将事件列表删去，以保证每次只有一个事件存在
        g_evene_queue.clear()


   