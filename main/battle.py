import pygame
import sys
from Setting import *
from Menu import defeat_menu,stop_menu
from Timer import Timer
from UI import button
from support import *
from sprites import boss,bullet
from add_event import add_event,g_evene_queue
from Player import Player_heart

class Battle:
    def __init__(self,line_start_tuple,line_end_tuple,toggle_battle,toggle_stop,player):
        #画障碍线的坐标
        self.line_start_tuple=line_start_tuple
        self.line_end_tuple=line_end_tuple
        #停止或开始游戏
        self.toggle_battle=toggle_battle
        self.toggle_stop=toggle_stop
        self.timer = Timer(200)
        #显示界面
        self.display_surface = pygame.display.get_surface()
#------------------
        self.battle1_sprites = pygame.sprite.Group()#用于添加战斗场景的组分
        self.bullets_spprites = pygame.sprite.Group()#单独创建一个储存场景子弹的组分
        self.collision_sprites = pygame.sprite.Group()#用于存储哪些组分需要有碰撞判定
#--------------------
        #添加心脏进入我的战斗
        self.Player_heart=Player_heart((400,300),self.display_surface,(0,200),(800,200))
        self.Player_heart.hp=100
        #添加boss进入我的战斗
        boss_frames = import_folder('../assets/demon1/react')
        boss((400,70),boss_frames,self.battle1_sprites)
        self.boss_hp=100

        self.battle1_sprites.add(self.Player_heart)

       
        #记录增加怪的次数
        self.bout_time=True
         #记录开始时间
        self.start_ticks=pygame.time.get_ticks()
        #用来传数据
        self.player=player    
    def battle(self,dt):
       
        self.display_surface.fill((0,0,0))
        if self.bout_time==True:
            for i in range(10):
                #添加子弹进入我的战斗（敌人方）
                self.bullet=bullet((0,200),(800,200))
                self.battle1_sprites.add(self.bullet)
                self.bullets_spprites.add(self.bullet)
                #添加进入需要判定碰撞的组
                self.collision_sprites.add(self.bullet)

            self.bout_time=False
        clock=pygame.time.Clock().tick(FPS)#帧率控制
        self.timer.update()
        #检测按键
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_f:
                    self.toggle_battle()
                elif event.key == pygame.K_ESCAPE:
                    self.start_ticks=pygame.time.get_ticks()
                    self.toggle_battle()
                    self.toggle_stop()
                    
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not self.timer.active:
            self.title_time=int((pygame.time.get_ticks()-self.start_ticks)/1000)
            self.battle1_sprites.update(dt)
            #判断是否发生碰撞
            hits=pygame.sprite.spritecollide(self.Player_heart,self.bullets_spprites,False)
            if hits:
                self.Player_heart.hp=self.Player_heart.hp-1
                if self.Player_heart.hp<=0:#没血了就进入失败画面
                    restart_flag=defeat_menu(self.display_surface)
                    return restart_flag

            self.battle1_sprites.draw(self.display_surface)
            if self.title_time%5==0:
                self.boss_hp=self.boss_hp-self.title_time*10

            if self.boss_hp<=0:
                    self.boss_hp=0
                    add_event(4)
                    g_evene_queue[-1]=4
                    self.bout_time=True
                    self.toggle_battle()
            pygame.draw.line(self.display_surface,(255,255,255),self.line_start_tuple,self.line_end_tuple)
#----------------------血量，时间的绘制---------------
            show_hp=button(0,0,0,30,30,660,550,f'HP: {self.Player_heart.hp}',30,255,255,255)
            show_time=button(0,0,0,30,30,150,550,f'TIME: {self.title_time}',30,255,255,255)
            show_hp.draw_button(self.display_surface)
            show_time.draw_button(self.display_surface)
            self.show_boss_hp=button(0,0,0,30,30,660,100,f'BOSSHP: {self.boss_hp}',30,255,255,255)
            self.show_boss_hp.draw_button(self.display_surface)
#----------------------------------------------------

    def update(self,dt):
        restart_flag=self.battle(dt)
        return restart_flag
#----------------------到此为止--------------


class Final_battle:
	def __init__(self):

		# 获取屏幕表面
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False
		
        # sprite group setup
		self.collision_sprites = pygame.sprite.Group()#控制场地大小
		self.all_sprites=pygame.sprite.Group()
        #攻击组分

		self.attack_sprites = pygame.sprite.Group()
		
        #初始化
		self.set_up()
		self.stop_menu=stop_menu(self.toggle_menu)
        #人物ui界面
		#self.ui = UI()
		
        #粒子效果
		#self.animation_player = AnimationPlayer()

	def set_up(self):
		self.player = Player_heart(
				pos = (400,500),
				group=[self.all_sprites],
				collision_sprites=self.collision_sprites,
                interaction=None,
                toggle_stop=self.toggle_menu,
                levelint=0
				)
		# Enemy(
		# 	monster_name,
		# 	(x,y),
		# 	[self.visible_sprites,self.attackable_sprites,self.all_moster_sprites],
		# 	self.obstacle_sprites,
		# 	self.damage_player,
		# 	self.trigger_death_particles,
		# 	self.add_exp)
	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.all_sprites])
	def trigger_death_particles(self,pos,particle_type):
		self.animation_player.create_particles(particle_type,pos,self.all_sprites)
	#def add_exp(self,amount):#增加或减少善恶值
		#self.player.exp += amount
	def toggle_menu(self):
		self.game_paused = not self.game_paused 
	def is_win(self):
		pass
	def run(self,dt):
		self.all_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		if self.game_paused:
			self.stop_menu.update()
		else:
			self.all_sprites.update(dt)
			self.all_sprites.enemy_update(self.player)
		self.is_win()
	

