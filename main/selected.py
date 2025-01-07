import pygame
import sys
from bornplace import born_place
from Level2 import Level2
from Level1 import Level1
from Menu import start_menu,win_menu
from add_event import add_event,g_evene_queue 
#
class selected:
    def __init__(self,player_will):
        self.player_will=player_will
        self.event_queue=add_event(0)
        self.born_place=born_place(player_will)
        self.Level2=Level2(player_will)
        self.win_menu=win_menu()
        self.Level1=Level1(player_will)
    def selected_level(self,dt,window):
        if self.flag==0:
            self.start_menu=start_menu(window)
            self.event_queue=add_event(self.start_menu)
        if self.flag == 1:
            self.event_queue=add_event(self.born_place.run(dt))
            self.player_will=self.born_place.get_player_will()
        if self.flag == 2:
            self.event_queue=add_event(self.Level1.run(dt))
            self.player_will=self.Level1.get_player_will()
        if self.flag == 3:
            self.event_queue=add_event(self.Level2.run(dt*2))
            self.player_will=self.Level2.get_player_will()
            print(self.player_will)
        if self.flag == 4:
            self.event_queue=add_event(self.win_menu.run())
        if self.flag==9:
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.Level1.toggle_menu()
    def add_event(self):
        self.flag=self.event_queue[-1]
    def run(self,dt,window):
        self.add_event()
        self.selected_level(dt,window)
#---------------到此为止---------      


    