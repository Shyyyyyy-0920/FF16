import pygame
import sys
from menu import menu
from battle import battle
from lose import lose
from map1 import darw_map
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
window.fill(WHITE)

pygame.display.flip()
flag=0#用于跳转界面
while 1 :
    match flag:
        case 0:
            flag=menu(window)#菜单界面
        case 1:
            flag=battle([0,200],[800,200])#主要战斗界面
        case 2:
            darw_map()
        case 3:#失败结算界面
            flag=lose(window)


   