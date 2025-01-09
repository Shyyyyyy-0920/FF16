import pygame
import sys
import chat

# 初始化 Pygame
pygame.init()
pygame.font.init()

# 设置窗口大小
width, height = 800, 600
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

# 主循环
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_TAB:
                trader_chat = chat.ChatBot("trader3")
                trader_chat.start()
#当前支持"trader3"  "trader1"  "flowey"
#仅仅实现了界面效果，对话检测与对应的效果还没弄。。。。
#关于自己debug了一个小时结果发现是自己之前的setting文件没更改后没保存这件事。。。



    # 更新屏幕显示
    pygame.display.flip()
    clock.tick(fps)