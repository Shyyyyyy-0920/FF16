import pygame
from Setting import *
from support import import_folder
#这里是按钮类
class button:
    def __init__(self,r1:int,g1:int,b1:int,height:int,width:int,inix:int,iniy:int,text:str,size:int,r2:int,g2:int,b2:int): 
        #矩形的三原色
        self.r1=r1
        self.g1=g1
        self.b1=b1
        old_color=(r1,g1,b1)
        self.old_color=old_color#用来记录按钮本来的颜色
        #矩形的长宽与左上角的坐标
        self.height=height
        self.width=width
        self.inix=inix
        self.iniy=iniy
        #矩形的文本与字号与字体
        self.text=text
        self.size=size
        #文字的三原色
        self.r2=r2
        self.g2=g2
        self.b2=b2
    def draw_button(self,window):#绘制按钮
        font=pygame.font.Font('../assets/font/DTM-Mono.otf',self.size)
        pygame.draw.rect(window,(self.r1,self.g1,self.b1),(self.inix,self.iniy,self.width,self.height))#绘制矩形
        text=font.render(self.text,True,(self.r2,self.g2,self.b2))
        tw1,th1=text.get_size()
        tx1=self.inix+self.width/2-tw1/2
        ty1=self.iniy+self.height/2-th1/2
        window.blit(text,(tx1,ty1))
        # pygame.display.update()
    def change_color(self,pos,window):
        m_x,m_y=pos
        btn_x,btn_y=self.inix,self.iniy
        btn_w,btn_h=self.width,self.height
        if btn_x<=m_x<=btn_x+btn_w and btn_y<=m_y<=btn_y + btn_h:
            self.r1=200
            self.g1=200
            self.b1=200
            self.draw_button(window)
            pygame.display.update()
            return True
        else:
            self.r1=self.old_color[0]
            self.g1=self.old_color[1]
            self.b1=self.old_color[2]
            self.draw_button(window)
            pygame.display.update()
            return False
#这是ui类
class UI:
	def __init__(self,player_will):
		# 普通设置
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
		self.player_will=player_will

		# 血条设置
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		self.will_value=pygame.Rect(350,560,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		self.bad_value=pygame.Rect(350,580,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		# 换武器的字典
		
		self.weapon_graphics=import_folder('../assets/graphics/weapons/ui')

		#转换魔术字典
		self.magic_graphics =import_folder('../assets/graphics/particles/magic_ui')
	def show_bar(self,current,max_amount,bg_rect,color):
		#画这个血条的背景
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		#百分比显示血量
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		#再画出血量
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):#画经验格子
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):#选项盒子的绘制
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):#选择武器的页面
		
		bg_rect = self.selection_box(10,510,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
		self.display_surface .blit(weapon_surf,weapon_rect)


	def magic_overlay(self,magic_index,has_switched):#选择魔法的页面
		bg_rect = self.selection_box(80,520,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface .blit(magic_surf,magic_rect)
		

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
		self.show_bar(self.player_will,10,self.will_value,ENERGY_COLOR)
		self.show_bar(10-self.player_will,10,self.bad_value,ENERGY_COLOR)
		self.show_exp(player.exp)
		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)

