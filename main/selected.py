import pygame
import sys
from bornplace import born_place
from Level2 import Level2
from Level1 import Level1
from Menu import start_menu,win_menu
from add_event import add_event
from battle import Final_battle
from final_scene import final_scene_False,final_scene_True
class selected:
    def __init__(self):
        self.old_flag=[]
        self.event_queue=add_event(0)
        self.start_menu=start_menu()
        self.born_place=born_place()
        self.Level2=Level2()
        self.win_menu=win_menu()
        self.Level1=Level1()
        self.Final_battle=Final_battle()
        self.final_scene_True=final_scene_True()
        self.final_scene_False=final_scene_False()
    def selected_level(self,dt):
        if self.flag==0:#菜单界面
            self.event_queue=add_event(self.start_menu.run())
        if self.flag == 1:#第一个出生场景
            self.event_queue=add_event(self.born_place.run(dt))
        if self.flag == 2:#第二个战斗场景
            self.event_queue=add_event(self.Level1.run(dt))
        if self.flag == 3:#第三个场景
            self.event_queue=add_event(self.Level2.run(dt))
        if self.flag == 4:#最终游戏胜利后跳转的场景
            self.event_queue=add_event(self.win_menu.run())
        if self.flag == 5:#开局的背景说明
            pass
            #self.event_queue=add_event(self.win_menu.run())
        if self.flag == 6:#最终boss战
            self.event_queue=add_event(self.Final_battle.run(dt))
        if self.flag == 7:#好结局
            self.event_queue=add_event(self.final_scene_True.run(dt))
        if self.flag == 8:#坏结局
            self.event_queue=add_event(self.final_scene_False.run(dt))
        if self.flag==9:
            pygame.quit()
            sys.exit()
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_m:
        #             self.Level1.toggle_menu()
    def add_event(self):
        self.flag=self.event_queue[-1]
    def run(self,dt):
        self.add_event()
        self.selected_level(dt)
#---------------到此为止---------      


    