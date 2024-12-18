import pygame
import sys
from menu import menu
pygame.init()
#创建游戏窗口
window=pygame.display.set_mode((800,600))
#C设置游戏标题
pygame.display.set_caption('真相之下')
 #设置游戏背景颜色
window.fill((255,255,255))
#加载图片
image1=pygame.image.load('photo/background_menu.png')
#渲染图片
window.blit(image1,(0,0))
pygame.display.flip()
menu(window)
