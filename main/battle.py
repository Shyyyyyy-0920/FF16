import pygame
from Setting import *
from Menu import defeat_menu,stop_menu
from UI import button,UI
from support import *
from sprites import boss,bullet,sans,attack1,light,block
from add_event import add_event,g_evene_queue
from Player import Player_heart
from will import player_will
from random import randint
from chat import ChatBot
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
        #来累计暂停期间的时间
        self.temp_paused_time=0
        self.time=0
        self.paused_time=0
        self.pause_start_time = 0  # 新增：用于记录暂停开始的时间点
        self.time_sign=False
        self.bout=1#用来记录阶段数
        self.use_time=0
        self.restart_flag=0
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
            self.bullet_image=pygame.image.load('../assets/Image/B_DOWN_w.png')
            self.bullet=bullet((0,200),(800,200),self.bullet_image)
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
                        self.bullet_image=pygame.image.load('../assets/Image/B_DOWN_w.png')
                        self.bullet=bullet((0,200),(800,200),self.bullet_image)
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
                        self.bullet_image=pygame.image.load('../assets/Image/B_DOWN_w.png')
                        self.bullet=bullet((0,200),(800,200),self.bullet_image)
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
                        self.bullet_image=pygame.image.load('../assets/Image/B_DOWN_w.png')
                        self.bullet=bullet((0,200),(800,200),self.bullet_image)
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
                pass
          elif self.boss_hp <=0:#打赢了boss，进入胜利对话
                pass
          #无论胜利与否，都会减少善良值增加邪恶值
    def update_will(self):
        self.new_player_will=self.player_will.get_player_will()
    def record_time(self):
        if not self.stop_active:
            self.pause_start_time = pygame.time.get_ticks()  # 记录暂停开始的时间
            
        else:
            self.paused_time = pygame.time.get_ticks() - self.pause_start_time # 累加暂停时间
            
        if self.paused_time !=0:
            self.time=self.paused_time+self.temp_paused_time

    def draw_ui(self):
        self.now_time=pygame.time.get_ticks()
        self.adjusted_time = self.now_time - self.time  # 使用调整后的时间
        self.time_clock=(self.adjusted_time-self.start_time)/1000
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
        self.record_time()
        self.draw_ui()
        self.playere_attack()
        self.damage_player()
        self.is_defeat()
        if not self.stop_active:
            self.all_sprites.update(dt)
            if self.restart_flag == 1:
                  self.reset()
                  self.start_time=pygame.time.get_ticks()
                  self.paused_time = 0  # 重置暂停时间
            self.restart_flag=0
            add_event(5)
            return 5
        else:
            self.menu_flag=self.Stop_Menu.update()
            if self.menu_flag == 1:
                  self.reset()
                  self.start_time=pygame.time.get_ticks()
                  self.paused_time = 0  # 重置暂停时间
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
        self.use_time=0
        #人物ui界面
        #self.ui = UI()
        #善恶值的UI
        self.player_will=player_will()
        self.ui=UI()
        #来累计暂停期间的时间
        self.temp_paused_time=0
        self.time=0
        self.paused_time=0
        self.pause_start_time = 0  # 新增：用于记录暂停开始的时间点
        self.time_sign=True
        #用来记录现在是第几阶段了
        self.bout=0
        self.flag=0##用来平凡切换状态创建一次性角色
        self.sign=0
        #粒子效果
        #self.animation_player = AnimationPlayer()
        #战斗音乐
        self.injury_sound = pygame.mixer.Sound('../assets/sound/injury.wav')
        self.injury_sound.set_volume(0.3)
        self.die_sound = pygame.mixer.Sound('../assets/sound/die.mp3')
        self.die_sound.set_volume(0.3)
        #人物对话部分
        self.game_paused = True#用于对话过程中暂停游戏
        self.sans0=ChatBot("sans0")
        self.sans1=ChatBot("sans1")
        self.sans2=ChatBot("sans2")

    def set_up(self):
        self.start_time=0
        self.player = Player_heart(
                pos = (400,450),
                group=[self.all_sprites],
                collision_sprites=self.collision_sprites,
                interaction=None,
                toggle_stop=None
                )
        #添加boss进入我的战斗
        boss_frames_body = import_folder('../assets/graphics/monsters/sans/Battle/common_body')
        self.boss_body=sans((400,65),boss_frames_body,self.all_sprites)
        boss_frames_head = import_folder('../assets/graphics/monsters/sans/Battle/common_head')
        self.boss_head=sans((435,10),boss_frames_head,self.all_sprites)
        self.boss_hp=100
    def damage_player(self,collision_sprites):
        #判断是否发生完美碰撞
        hits=pygame.sprite.spritecollide(self.player,collision_sprites,False,pygame.sprite.collide_mask)
        for sprite in hits:
            if sprite is not self.player:
                if self.player.vulnerable:
                    self.player.hp -= 5
                    self.player.vulnerable=False
                    self.player.hurt_time = pygame.time.get_ticks()
    def sans_states_attack(self,bout):
        if bout == 0:
            #四条龙喷激光
            if self.flag == 0:
                if self.sign==0:
                    for i in range(4):
                        self.light=light((102,200+100*i),[self.all_sprites,self.attack_sprites],'right')
                        self.sans_attack1_frames = import_folder('../assets/graphics/monsters/sans/Attacks/battle_1')
                        self.sans_attack=attack1((70,200+100*i),self.sans_attack1_frames,[self.all_sprites,self.attack_sprites])#怪头
                        self.sign=1
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 1500:  # 如果存活时间超过2秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=1
            if self.flag == 1:
                if self.sign==1:
                    for i in range(4):
                        self.light=light((100+200*i,200),[self.all_sprites,self.attack_sprites],'down')
                        self.sans_attack1_frames = import_folder('../assets/graphics/monsters/sans/Attacks/battle_1')
                        self.sans_attack=attack1((100+200*i,170),self.sans_attack1_frames,[self.all_sprites,self.attack_sprites])#怪头
                        self.sign=2
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 1500:  # 如果存活时间超过2秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=2
            if self.flag == 2:
                if self.sign==2:
                    for i in range(4):
                        self.light=light((700,200+100*i),[self.all_sprites,self.attack_sprites],'left')
                        self.sans_attack1_frames = import_folder('../assets/graphics/monsters/sans/Attacks/battle_1')
                        self.sans_attack=attack1((720,200+100*i),self.sans_attack1_frames,[self.all_sprites,self.attack_sprites])#怪头
                        self.sign=0
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 2000:  # 如果存活时间超过1秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=0
        elif bout == 1:
            #弹幕躲避
            if self.flag == 0:
                if self.sign==0:
                    for i in range(10):
                        #添加子弹进入我的战斗（敌人方）
                        self.bullet_image=pygame.image.load('../assets/graphics/monsters/sans/Attacks/spr_s_boneloop_out_0.png')
                        self.bullet=bullet((100,200),(700,200),self.bullet_image)
                        self.all_sprites.add(self.bullet)
                        self.attack_sprites.add(self.bullet)
                        self.sign=1
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 2500:  # 如果存活时间超过2.5秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=1
            if self.flag == 1:
                if self.sign==1:
                    for i in range(10):
                        #添加子弹进入我的战斗（敌人方）
                        path=f'../assets/graphics/monsters/sans/Attacks/{randint(0,3)}.png'
                        self.bullet_image=pygame.image.load(path)
                        self.bullet=bullet((100,200),(700,200),self.bullet_image)
                        self.all_sprites.add(self.bullet)
                        self.attack_sprites.add(self.bullet)
                        self.sign=0
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 2500:  # 如果存活时间超过2.5秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=0
        elif bout == 2:
            if self.flag == 0:
                if self.sign==0:
                    block_up1=block((710,200),[self.all_sprites,self.attack_sprites],0,'left')
                    block_up2=block((560,200),[self.all_sprites,self.attack_sprites],0,'left')
                    block_up3=block((900,200),[self.all_sprites,self.attack_sprites],2,'left')
                    block_up4=block((-100,200),[self.all_sprites,self.attack_sprites],2,'right')
                    block_bottom1=block((720,500),[self.all_sprites,self.attack_sprites],1,'left')
                    block_bottom2=block((1,438),[self.all_sprites,self.attack_sprites],2,'right')
                    block_bottom3=block((-60,400),[self.all_sprites,self.attack_sprites],0,'right')
                    block_bottom4=block((950,400),[self.all_sprites,self.attack_sprites],3,'left')
                    self.sign=1
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 2500:  # 如果存活时间超过秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=1
            elif self.flag==1:
                if self.sign==1:
                    block_up1=block((-150,200),[self.all_sprites,self.attack_sprites],0,'right')
                    block_up2=block((3,200),[self.all_sprites,self.attack_sprites],0,'right')
                    block_up3=block((1,438),[self.all_sprites,self.attack_sprites],2,'right')
                    block_up4=block((570,340),[self.all_sprites,self.attack_sprites],2,'left')
                    block_bottom1=block((-199,500),[self.all_sprites,self.attack_sprites],1,'right')
                    block_bottom1=block((40,500),[self.all_sprites,self.attack_sprites],1,'right')
                    block_bottom1=block((-199,470),[self.all_sprites,self.attack_sprites],1,'right')
                    block_bottom2=block((900,200),[self.all_sprites,self.attack_sprites],2,'left')
                    block_bottom3=block((870,440),[self.all_sprites,self.attack_sprites],0,'left')
                    block_bottom3=block((990,440),[self.all_sprites,self.attack_sprites],0,'left')
                    for i in range(9):
                        block_bottom4=block((100-35*i,400),[self.all_sprites,self.attack_sprites],3,'right')
                    self.sign=0
                self.damage_player(self.attack_sprites)
                for sprite in self.attack_sprites:  # 使用 copy() 避免迭代过程中改变集合大小的问题
                    if self.battle_start_time - sprite.creat_time >= 2500:  # 如果存活时间超过秒
                        sprite.kill()  # 移除该对象
                if len(self.attack_sprites) == 0:
                    self.flag=0
        
    def sans_states_animations(self):
        if self.title_time%5==0:
            if self.title_time /5==1 :#一阶段结束
                self.boss_hp = 70
                self.boss_head.kill()
                self.boss_body.kill()
                boss_frames_body = import_folder('../assets/graphics/monsters/sans/Battle/attack1_body')
                self.boss_body=sans((395,0),boss_frames_body,self.all_sprites)
                boss_frames_head = import_folder('../assets/graphics/monsters/sans/Battle/attack1_head')
                self.boss_head=sans((435,10),boss_frames_head,self.all_sprites)
                self.injury_sound.play()
                self.bout=1
                self.sans_states_attack(self.bout)
                self.toggle_talk()
            elif self.title_time / 5==2:#二阶段结束
                self.boss_hp =30
                self.boss_head.kill()
                self.boss_body.kill()
                boss_frames_body = import_folder('../assets/graphics/monsters/sans/Battle/attack2_body')
                self.boss_body=sans((395,0),boss_frames_body,self.all_sprites)
                boss_frames_head = import_folder('../assets/graphics/monsters/sans/Battle/attack2_head')
                self.boss_head=sans((435,10),boss_frames_head,self.all_sprites)
                self.injury_sound.play()
                self.bout=2
                self.sans_states_attack(self.bout)
                self.toggle_talk()
            elif self.title_time / 5 == 3:#三阶段结束，进入对话
                self.boss_hp =0
                self.boss_head.kill()
                self.boss_body.kill()
                boss_frames_body = import_folder('../assets/graphics/monsters/sans/Battle/injury_body')
                self.boss_body=sans((400,60),boss_frames_body,self.all_sprites)
                boss_frames_head = import_folder('../assets/graphics/monsters/sans/Battle/injury_head')
                self.boss_head=sans((435,10),boss_frames_head,self.all_sprites)
                self.injury_sound.play()
                self.bout=3
                self.toggle_talk()
                #self.sans_states_attack(self.bout)
    def sans_talk(self):
        if self.bout==0:
            self.sans0.start(True,self.toggle_talk)
        elif self.bout == 1:
            self.sans1.start(True,self.toggle_talk)
        elif self.bout == 2:
            self.sans2.start(True,self.toggle_talk)
    def toggle_talk(self):
        self.game_paused = not self.game_paused 
    def record_time(self):
        if not self.game_paused:
            self.pause_start_time = pygame.time.get_ticks()  # 记录暂停开始的时间
            
        else:
            self.paused_time = pygame.time.get_ticks() - self.pause_start_time # 累加暂停时间
            #print(self.paused_time)
        if self.paused_time !=0:
            self.time=self.paused_time+self.temp_paused_time

    def is_win(self):
        pass
    def draw_ui(self):
        self.new_player_will=self.player_will.get_player_will()
        self.now_time=pygame.time.get_ticks()
        self.adjusted_time = self.now_time - self.time  # 使用调整后的时间
        self.time_clock=(self.adjusted_time-self.start_time)/1000

        self.title_time=round(self.time_clock)
        #----------------------血量，时间的绘制---------------
        self.show_hp=button(0,0,0,30,30,660,550,f'HP: {self.player.hp}',30,255,0,0)
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
        
    def bgm_play(self):
        if self.use_time==0:
              self.use_time+=1
              pygame.mixer.music.fadeout(1000)
              pygame.mixer.quit()
              pygame.init()
              pygame.mixer.music.load('../assets/audio/in_battle.mp3')
              pygame.mixer.music.set_volume(0.3)              
              pygame.mixer.music.play(loops=-1)
    def run(self,dt):
        self.battle_start_time=pygame.time.get_ticks()
        self.bgm_play()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.record_time()#记录暂停的时候的时间
        self.draw_ui()#画UI
        self.sans_states_animations()#画出boss每个阶段的动画,并且判断现在是否进入新阶段的对话
        self.is_win()#判断是否胜利
        print(self.start_time)
        if not self.game_paused:
            self.all_sprites.update(dt)
            add_event(6)
        else:
            self.sans_talk()
            if  not self.game_paused:
                self.temp_paused_time+=self.paused_time
                self.paused_time = 0  # 重置暂停时间
                if self.time_sign:#调控第一次进入
                    self.start_time=pygame.time.get_ticks()
                    self.time_sign=False
                    self.paused_time = 0  # 重置暂停时间
                    self.temp_paused_time=0
                    self.time=0
  
        if g_evene_queue[-1]==6:
              return 6
        else:
              pass
#----------------------到此为止--------------