import pygame
import sys
from Setting import *
from Menu import defeat_menu,stop_menu
from UI import button,UI
from support import *
from sprites import boss,bullet,sans,attack1
from add_event import add_event,g_evene_queue
from Player import Player_heart
from will import player_will

class Trader_Battle:
    def __init__(self):
        #画障碍线的坐标
        self.line_start_tuple=(0,200)
        self.line_end_tuple=(800,200)
        #显示界面
        self.display_surface = pygame.display.get_surface()
#------------------
        self.all_sprites = pygame.sprite.Group()#用于添加战斗场景的组分
        self.bullets_sprites = pygame.sprite.Group()#单独创建一个储存场景子弹的组分
        self.collision_sprites = pygame.sprite.Group()#用于存储哪些组分需要有碰撞判定
        self.set_up()
#--------------------
        #暂停界面
        self.Stop_Menu=stop_menu(self.toggle_stop)
        self.stop_active = False
        #善恶值的UI
        self.player_will=player_will()
        self.ui=UI()

        self.restart_flag=2
        self.use_time=0
        self.bout=1
        #声音设置
        self.injury_sound = pygame.mixer.Sound('../assets/sound/injury.wav')
        self.injury_sound.set_volume(0.3)
        self.die_sound = pygame.mixer.Sound('../assets/sound/die.mp3')
        self.die_sound.set_volume(0.3)

    def set_up(self):
        
        #添加心脏进入我的战斗
        self.start_time=0
        self.Player_heart=Player_heart((400,500),self.all_sprites,self.collision_sprites,None,self.toggle_stop)
        for i in range(5):
            #添加子弹进入我的战斗（敌人方）
            self.bullet=bullet((0,200),(800,200))
            self.all_sprites.add(self.bullet)
            self.bullets_sprites.add(self.bullet)
            #添加进入需要判定碰撞的组
            self.collision_sprites.add(self.bullet)
        #添加boss进入我的战斗
        boss_frames = import_folder('../assets/demon1/react')
        self.boss1=boss((400,70),boss_frames,self.all_sprites)
        self.boss_hp=100
    def toggle_stop(self):
        self.stop_active = not self.stop_active
    def damage_player(self):
        #判断是否发生完美碰撞
        hits=pygame.sprite.spritecollide(self.Player_heart,self.bullets_sprites,False,pygame.sprite.collide_mask)
        for sprite in hits:
            if sprite is not self.Player_heart:
                if self.Player_heart.vulnerable:
                    self.Player_heart.hp -= 50
                    self.Player_heart.vulnerable=False
                    self.Player_heart.hurt_time = pygame.time.get_ticks()
               
    def playere_attack(self):
        if self.title_time%5==0:
            if self.title_time /5==1 :
                self.boss_hp = 70
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/attack')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                if self.bout == 1:
                    for i in range(5):
                        #添加子弹进入我的战斗（敌人方）
                        self.bullet=bullet((0,200),(800,200))
                        self.all_sprites.add(self.bullet)
                        self.bullets_sprites.add(self.bullet)
                        #添加进入需要判定碰撞的组
                        self.collision_sprites.add(self.bullet)
                        self.bout=2
            elif self.title_time / 5==2:
                self.boss_hp =30
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/injury')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                if self.bout == 2:
                    for i in range(5):
                        #添加子弹进入我的战斗（敌人方）
                        self.bullet=bullet((0,200),(800,200))
                        self.all_sprites.add(self.bullet)
                        self.bullets_sprites.add(self.bullet)
                        #添加进入需要判定碰撞的组
                        self.collision_sprites.add(self.bullet)
                        self.bout=3
            elif self.title_time / 5 == 3:
                self.boss_hp =5
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/injury')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                if self.bout == 3:
                    for i in range(5):
                        #添加子弹进入我的战斗（敌人方）
                        self.bullet=bullet((0,200),(800,200))
                        self.all_sprites.add(self.bullet)
                        self.bullets_sprites.add(self.bullet)
                        #添加进入需要判定碰撞的组
                        self.collision_sprites.add(self.bullet)
                        self.bout=4
            elif self.title_time / 5 == 4:
                self.boss_hp =0
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/die')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.die_sound.play()
                if self.bout == 4:
                    for sprite in self.bullets_sprites:
                        sprite.kill()
            
    def is_defeat(self):
        if self.Player_heart.hp<=0:#没血了就进入失败画面
            self.restart_flag=defeat_menu(self.display_surface)
    def over(self):#这是结束后的场景，无论失败还是胜利
          if self.Player_heart.hp<=0:#没血了就进入失败画面,失败的对话
                add_event()
          elif self.boss_hp <=0:#打赢了boss，进入胜利对话
                pass
          #无论胜利与否，都会减少善良值增加邪恶值
    def update_will(self):
        self.new_player_will=self.player_will.get_player_will()
    def draw_ui(self):
        self.now_time=pygame.time.get_ticks()
        self.time_clock=(self.now_time-self.start_time)/1000
        self.title_time=round(self.time_clock)
        #----------------------血量，时间的绘制---------------
        self.show_hp=button(0,0,0,30,30,660,550,f'HP: {self.Player_heart.hp}',30,255,255,255)
        self.show_time=button(0,0,0,30,30,150,550,f'TIME: {self.title_time}',30,255,255,255)
        self.show_boss_hp=button(0,0,0,30,30,660,100,f'BOSSHP: {self.boss_hp}',30,255,255,255)
        self.show_hp.draw_button(self.display_surface)
        self.show_time.draw_button(self.display_surface)
        self.show_boss_hp.draw_button(self.display_surface)
        self.ui.show_bar(self.new_player_will,10,self.ui.will_value,PLAYER_WILL_COLOR)
        self.ui.show_bar(10-self.new_player_will,10,self.ui.bad_value,PLAYER_BAD_COLOR)
        pygame.draw.line(self.display_surface,(255,255,255),(100,200),(700,200))
        pygame.draw.line(self.display_surface,(255,255,255),(100,200),(100,530))
        pygame.draw.line(self.display_surface,(255,255,255),(700,200),(700,530))
        pygame.draw.line(self.display_surface,(255,255,255),(100,530),(700,530))
          
    def reset(self):
        self.all_sprites.empty()
        self.bullets_sprites.empty()
        self.collision_sprites.empty()
        self.set_up()
    def run(self,dt):
        self.update_will()
        if self.use_time==0:
              self.start_time=pygame.time.get_ticks()
              self.use_time+=1
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.draw_ui()
        self.playere_attack()
        self.damage_player()
        
        self.is_defeat()
        if not self.stop_active:
            self.all_sprites.update(dt)
            if self.restart_flag == 1:
                  print(self.restart_flag)
                  self.reset()
                  self.start_time=pygame.time.get_ticks()
            self.restart_flag=2
            add_event(5)
            return 5
        else:
            self.start_time+=2.475
            self.menu_flag=self.Stop_Menu.update()
            if self.menu_flag == 1:
                  self.reset()
                  self.start_time=pygame.time.get_ticks()
                  add_event(5)
                  return 5
            elif self.menu_flag == 2:
                  add_event(9)
                  return 9
        if g_evene_queue[-1]==5:
              return 5
        else:
              pass

class Final_battle:
    def __init__(self):

        # 获取屏幕表面
        self.display_surface = pygame.display.get_surface()
        
        
        # sprite group setup
        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites=pygame.sprite.Group()
        #攻击组分

        self.attack_sprites = pygame.sprite.Group()
        
        #初始化
        self.set_up()
        self.stop_menu=stop_menu(self.toggle_menu)
        self.game_paused = False
        self.use_time=0
        #人物ui界面
        #self.ui = UI()
         #善恶值的UI
        self.player_will=player_will()
        self.ui=UI()
        
        #粒子效果
        #self.animation_player = AnimationPlayer()
        #战斗音乐
        self.battle_sound = pygame.mixer.Sound('../assets/audio/in_battle.mp3')
        self.battle_sound.set_volume(0.3)
        self.injury_sound = pygame.mixer.Sound('../assets/sound/injury.wav')
        self.injury_sound.set_volume(0.3)
        self.die_sound = pygame.mixer.Sound('../assets/sound/die.mp3')
        self.die_sound.set_volume(0.3)

    def set_up(self):
        self.start_time=0
        self.player = Player_heart(
                pos = (400,500),
                group=[self.all_sprites],
                collision_sprites=self.collision_sprites,
                interaction=None,
                toggle_stop=self.toggle_menu
                )
         #添加boss进入我的战斗
        boss_frames_head = import_folder('../assets/graphics/monsters/sans/Battle/common_head')
        self.boss_head=sans((435,10),boss_frames_head,self.all_sprites)
        boss_frames_body = import_folder('../assets/graphics/monsters/sans/Battle/common_body')
        self.boss_body=sans((400,70),boss_frames_body,self.all_sprites)
        self.boss_hp=100
        for i in range(6):
            self.sans_attack1_frames = import_folder('../assets/graphics/monsters/sans/Attacks/battle_1')
            self.sans_attack=attack1((70,200+100*i),self.sans_attack1_frames,self.display_surface,self.all_sprites,self.attack_sprites,pygame.math.Vector2(1,0))
    def damage_player(self,amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    def boss_states(self):
        pass
    def update_will(self):
        self.new_player_will=self.player_will.get_player_will()
    def playere_attack(self):
        if self.title_time%5==0:
            if self.title_time /5==1 :
                self.boss_hp = 70
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/attack')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                # if self.bout == 1:
                #     for i in range(5):
                #         #添加子弹进入我的战斗（敌人方）
                #         self.bullet=bullet((0,200),(800,200))
                #         self.all_sprites.add(self.bullet)
                #         self.bullets_sprites.add(self.bullet)
                #         #添加进入需要判定碰撞的组
                #         self.collision_sprites.add(self.bullet)
                #         self.bout=2
            elif self.title_time / 5==2:
                self.boss_hp =30
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/injury')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                # if self.bout == 2:
                #     for i in range(5):
                #         #添加子弹进入我的战斗（敌人方）
                #         self.bullet=bullet((0,200),(800,200))
                #         self.all_sprites.add(self.bullet)
                #         self.bullets_sprites.add(self.bullet)
                #         #添加进入需要判定碰撞的组
                #         self.collision_sprites.add(self.bullet)
                #         self.bout=3
            elif self.title_time / 5 == 3:
                self.boss_hp =5
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/injury')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.injury_sound.play()
                # if self.bout == 3:
                #     for i in range(5):
                #         #添加子弹进入我的战斗（敌人方）
                #         self.bullet=bullet((0,200),(800,200))
                #         self.all_sprites.add(self.bullet)
                #         self.bullets_sprites.add(self.bullet)
                #         #添加进入需要判定碰撞的组
                #         self.collision_sprites.add(self.bullet)
                #         self.bout=4
            elif self.title_time / 5 == 4:
                self.boss_hp =0
                self.boss1.kill()
                boss_frames = import_folder('../assets/demon1/die')
                self.boss1=boss((400,70),boss_frames,self.all_sprites)
                self.die_sound.play()
                # if self.bout == 4:
                #     for sprite in self.bullets_sprites:
                #         sprite.kill()
    def toggle_menu(self):
        self.game_paused = not self.game_paused 
    def is_win(self):
        pass
    def draw_ui(self):
        self.now_time=pygame.time.get_ticks()
        self.time_clock=(self.now_time-self.start_time)/1000

        self.title_time=round(self.time_clock)
        #----------------------血量，时间的绘制---------------
        self.show_hp=button(0,0,0,30,30,660,550,f'HP: {self.player.hp}',30,255,255,255)
        self.show_time=button(0,0,0,30,30,150,550,f'TIME: {self.title_time}',30,255,255,255)
        self.show_boss_hp=button(0,0,0,30,30,660,100,f'BOSSHP: {self.boss_hp}',30,255,255,255)
        self.show_hp.draw_button(self.display_surface)
        self.show_time.draw_button(self.display_surface)
        self.show_boss_hp.draw_button(self.display_surface)
        self.ui.show_bar(self.new_player_will,10,self.ui.will_value,PLAYER_WILL_COLOR)
        self.ui.show_bar(10-self.new_player_will,10,self.ui.bad_value,PLAYER_BAD_COLOR)
        pygame.draw.line(self.display_surface,(255,255,255),(100,200),(700,200))
        pygame.draw.line(self.display_surface,(255,255,255),(100,200),(100,530))
        pygame.draw.line(self.display_surface,(255,255,255),(700,200),(700,530))
        pygame.draw.line(self.display_surface,(255,255,255),(100,530),(700,530))
    def reset(self):
        self.all_sprites.empty()
        self.attack_sprites.empty()
        self.collision_sprites.empty()
        self.set_up()
    def run(self,dt):
        self.update_will()
        if self.use_time==0:
              self.start_time=pygame.time.get_ticks()
              self.use_time+=1
              pygame.mixer.music.stop()
              self.battle_sound.play(loops=-1)
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.draw_ui()
        self.is_win()
        if not self.game_paused:
            self.all_sprites.update(dt)
            add_event(6)
            return 6
        else:
            self.start_time+=2.465
            self.menu_flag=self.stop_menu.update()
            if self.menu_flag == 1:
                  self.reset()
                  self.start_time=pygame.time.get_ticks()
                  add_event(6)
                  return 6
            elif self.menu_flag == 2:
                  add_event(9)
                  return 9
        if g_evene_queue[-1]==6:
              return 6
        else:
              pass
#----------------------到此为止--------------