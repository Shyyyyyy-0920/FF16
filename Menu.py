import pygame
from Setting import *
from Timer import Timer
from button import button
import sys
class Menu:
	def __init__(self, player, toggle_menu):

		# 常规设置
		self.player = player
		self.toggle_menu = toggle_menu
		self.display_surface = pygame.display.get_surface()#获取表面信息
		self.font = pygame.font.Font('../assets/font/DTM-Mono.otf', 30)#装载字体

		# 选项设置
		self.width = 400
		self.space = 10
		self.padding = 8

		# 进入界面
		self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
		self.sell_border = len(self.player.item_inventory) - 1
		self.setup()

		# 换行移动
		self.index = 0
		self.timer = Timer(200)

	def display_money(self):#用于展示现在玩家的金额，总的来说是读取金额数再显示出
		text_surf = self.font.render(f'${self.player.money}', False, 'Black')#这里是将字打出来
		text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2,SCREEN_HEIGHT - 20))#获取字的矩形框大小

		pygame.draw.rect(self.display_surface,'White',text_rect.inflate(10,10),0,4)#在字的周围画上矩形框
		self.display_surface.blit(text_surf,text_rect)#装载更新

	def setup(self):

		# 创建新的文本表面
		self.text_surfs = []
		self.total_height = 0

		for item in self.options:#option在上文已经定义，这里就可以建立多条矩形框，再分层
			text_surf = self.font.render(item, False, 'Black')
			self.text_surfs.append(text_surf)
			self.total_height += text_surf.get_height() + (self.padding * 2)

		self.total_height += (len(self.text_surfs) - 1) * self.space
		self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
		self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top,self.width,self.total_height)

		# 买或者卖的文本画面
		self.buy_text = self.font.render('buy',False,'Black')
		self.sell_text =  self.font.render('sell',False,'Black')

	def input(self):#一些输入和引起的反应
		keys = pygame.key.get_pressed()
		self.timer.update()
		if keys[pygame.K_ESCAPE]:
			self.toggle_menu()

		if not self.timer.active:
			if keys[pygame.K_w]:
				self.index -= 1
				self.timer.activate()

			if keys[pygame.K_s]:
				self.index += 1
				self.timer.activate()

			if keys[pygame.K_SPACE]:
				self.timer.activate()

				# get item
				current_item = self.options[self.index]

				# sell
				if self.index <= self.sell_border:
					if self.player.item_inventory[current_item] > 0:
						self.player.item_inventory[current_item] -= 1
						self.player.money += SALE_PRICES[current_item]

				# buy
				else:
					seed_price = PURCHASE_PRICES[current_item]
					if self.player.money >= seed_price:
						self.player.seed_inventory[current_item] += 1
						self.player.money -= PURCHASE_PRICES[current_item]



		# 可以上下滚动保证不出界
		if self.index < 0:
			self.index = len(self.options) - 1
		if self.index > len(self.options) - 1:
			self.index = 0

	def show_entry(self, text_surf, amount, top, selected):#展示画面

		# 背景
		bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

		# 文字
		text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20,bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)

		#数量
		amount_surf = self.font.render(str(amount), False, 'Black')
		amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20,bg_rect.centery))
		self.display_surface.blit(amount_surf, amount_rect)

		#选项
		if selected:
			pygame.draw.rect(self.display_surface,'black',bg_rect,4,4)
			if self.index <= self.sell_border: # sell
				pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.sell_text,pos_rect)
			else: # buy
				pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.buy_text,pos_rect)

	def update(self):
		self.input()
		self.display_money()

		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
			amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
			amount = amount_list[text_index]
			self.show_entry(text_surf, amount, top, self.index == text_index)
#--------------游戏失败界面
def defeat_menu(window,restart_game):
    window.fill((255,255,255))
    #加载图片
    image1=pygame.image.load('../assets/Image/结束界面背景.jpg')
    # 渲染图片
    window.blit(image1,(0,0))
    pygame.display.update()
    restart_button=button(255,255,255,70,350,240,60,'RESTART GAME',45,0,0,0)
    quiet_button=button(255,255,255,70,250,300,440,'QUIET ',45,0,0,0)
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
                    restart_game([0,200],[800,200])
                elif quiet_key==1:#判断是否按到了退出游戏
                    sys.exit()

#------------------------------------------

#--------------------------------------游戏开始界面
def start_menu(window):
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('../assets/photo/background_menu.png')
    # 渲染图片
    window.blit(image1,(0,0))
    pygame.display.update()
    start_button=button(0,0,0,70,247,280,280,'start game',45,255,255,255)
    set_button=button(0,0,0,70,250,280,360,'set',45,255,255,255)
    quiet_button=button(0,0,0,70,250,300,440,'QUIET ',45,255,255,255)
    while 1:
    #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
#----------开始界面三个按钮的建立----------------------------------------
            start_button.draw_button(window)
            set_button.draw_button(window)
            quiet_button.draw_button(window)
            start_key=start_button.change_color(pygame.mouse.get_pos(),window)
            set_key=set_button.change_color(pygame.mouse.get_pos(),window)
            quiet_key=quiet_button.change_color(pygame.mouse.get_pos(),window)
#----------=====================----------------------------------------
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_key==True:#判断是否按到了开始游戏
                    window.fill((255,255,255))
                    pygame.display.update()
                    return 1
                elif set_key==1:#判断是否按到了设置
                    window.fill((255,255,255))
                    pygame.display.update()
                    return 2
                elif quiet_key==1:#判断是否按到了退出游戏
                    return 3

#------------------以下是暂停界面
def stop_menu():

    #第一个按钮，继续游戏
    continue_button=button(0,0,0,70,247,280,280,'CONTINUE',45,255,255,255)

    #第二个按钮，重新开始
    restart_button=button(0,0,0,70,250,300,360,'RESTART',45,255,255,255)#我上面写了button需要传入的参数

    #第三个按钮，返回菜单
    back_menu_button=button(0,0,0,70,250,300,440,'BACK ',45,255,255,255)

    #第四G个按钮，退出游戏
    quiet_button=button(0,0,0,70,250,300,520,'QUIET ',45,255,255,255)

    #创建完按钮写出对应的事件，再做判断
    #注意命名规范与注释的必要



#________________------------------------------------------
