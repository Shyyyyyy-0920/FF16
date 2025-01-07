import pygame
from Setting import *
pygame.init()
font = pygame.font.Font('../assets/font/DTM-Mono.otf', 30)

def will(info,y = 0, x = 750):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'white')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)
