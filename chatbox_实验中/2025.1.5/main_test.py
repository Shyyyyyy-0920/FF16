import pygame
import sys
import chat1


pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                break
            if event.key == pygame.K_t:
                trader_chat = chat1.Chatbot("trader in 1")
                trader_chat.start()

    pygame.display.flip()
    clock.tick(fps)