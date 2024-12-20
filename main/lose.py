import pygame
import sys
import button#按钮需要传入这几个参数，1.鼠标位置2.三个三原色，3.矩形高和宽（注意高在前面）4.矩形左上角的坐标5.文字内容6。文字大小7.3个文字的三原色
WHITE=(255,255,255)
def lose(window):
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('arrests/Image/结束界面背景.jpg')
    # 渲染图片
    window.blit(image1,(0,0))
    pygame.display.update()
    restart_button=button.button(255,255,255,70,350,240,60,'RESTART GAME',45,0,0,0)
    quiet_button=button.button(255,255,255,70,250,300,440,'QUIET ',45,0,0,0)
    while 1:
    #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
#----------开始界面三个按钮的建立----------------------------------------
            restart_button.draw_button(window)
            quiet_button.draw_button(window)
            start_key=restart_button.change_color(pygame.mouse.get_pos(),window)
            quiet_key=quiet_button.change_color(pygame.mouse.get_pos(),window)
#----------=====================----------------------------------------
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_key==True:#判断是否按到了重新游戏
                    window.fill((255,255,255))
                    pygame.display.update()
                    return 2
                elif quiet_key==1:#判断是否按到了退出游戏
                    sys.exit()