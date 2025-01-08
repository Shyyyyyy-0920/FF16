import pygame
from Setting import *
from Timer import Timer
from UI import button
import sys
from add_event import add_event

#这个类主要是各个菜单界面的创建和绘制与反应
class Menu:
	def __init__(self, player, toggle_menu):

		# 常规设置
		self.player = player#传入一个角色，下面会用到读取角色的属性，比如身上的物品，善恶值这些
		self.toggle_menu = toggle_menu#用来执行是否关闭或打开界面
		self.display_surface = pygame.display.get_surface()#获取表面信息
		self.font = pygame.font.Font('../assets/font/DTM-Mono.otf', 30)#装载字体

		# 选项设置
		self.width = 400
		self.space = 10
		self.padding = 8

		# 进入界面
		self.options = list(self.player.item_inventory.keys())+list(self.player.talk_inventory.keys())#一共有这么多行，可以买和卖
		self.give_border = len(self.player.item_inventory) - 1
		self.setup()

		# 换行移动
		self.index = 0
		self.timer = Timer(200)
		#商人物品的储存
		self.trader_item_inventory = {
			'wood':   2,
			'apple':  2,
			'corn':   2,
			'tomato': 2,
		}
		#设置音乐
		self.switch_up = pygame.mixer.Sound('../assets/audio/Menu3.wav')
		self.switch_up.set_volume(0.8)
		self.switch_down=pygame.mixer.Sound('../assets/audio/Menu7.wav')
		self.switch_down.set_volume(0.8)
		self.menu_fix=pygame.mixer.Sound('../assets/audio/Menu12.wav')
		self.menu_fix.set_volume(0.8)
		self.menu_loot=pygame.mixer.Sound('../assets/audio/Menu11.wav')
		self.menu_loot.set_volume(0.8)
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

		# 文本画面
		self.talk_text = self.font.render('talk',False,'Black')
		self.give_text =  self.font.render('give/loot',False,'Black')

	def input(self):#一些输入和引起的反应
		keys = pygame.key.get_pressed()
		self.timer.update()
		if keys[pygame.K_ESCAPE]:
			self.toggle_menu()

		if not self.timer.active:
			if keys[pygame.K_w]:
				self.index -= 1
				self.timer.activate()
				self.switch_up.play()

			if keys[pygame.K_s]:
				self.index += 1
				self.timer.activate()
				self.switch_down.play()

			if keys[pygame.K_SPACE]:#这里可以进行转换，如果赠送，那么增加善良值，如果全部抢夺，那么增加邪恶值
				self.timer.activate()
				self.menu_fix.play()

				# get item
				current_item = self.options[self.index]

				#赠送
				if self.index <= self.give_border:
					if self.player.item_inventory[current_item] > 0:
						self.player.item_inventory[current_item] -= 1
						self.trader_item_inventory[current_item] +=1
						#self.player.money += SALE_PRICES[current_item]#这里写善恶值增加

				#聊天
				else:
					add_event(5)
			if keys[pygame.K_LCTRL]:
				self.timer.activate()
				self.menu_loot.play()
				# get item
				current_item = self.options[self.index]
				#抢夺
				if self.index <= self.give_border:
					if self.player.item_inventory[current_item] > 0 and self.trader_item_inventory[current_item]>0:
						self.player.item_inventory[current_item] += 1
						self.trader_item_inventory[current_item] -=1
				else:#聊天
					add_event(5)


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
			if self.index <= self.give_border: #give
				pos_rect = self.give_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.give_text,pos_rect)
			else: #talk
				pos_rect = self.talk_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.talk_text,pos_rect)

	def update(self):
		self.input()
		self.display_money()
		#print(self.player.item_inventory,self.trader_item_inventory)
		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
			amount_list = list(self.player.item_inventory.values())+ list(self.player.talk_inventory.values())
			amount = amount_list[text_index]
			self.show_entry(text_surf, amount, top, self.index == text_index)

class Upgrade:
	def __init__(self,player):
		#普通设置
		self.display_surface = pygame.display.get_surface()
		self.player = player#传入玩家类
		self.attribute_nr = len(player.stats)#玩家状态一共这么长
		self.attribute_names = list(player.stats.keys())
		self.max_values = list(player.max_stats.values())
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		self.height = self.display_surface.get_size()[1] * 0.8
		self.width = self.display_surface.get_size()[0] // 6
		self.create_items()

		#选择系统
		self.selection_index = 0
		self.selection_time = None
		#用于调控能否开始移动
		self.can_move = True
		self.switch_left = pygame.mixer.Sound('../assets/audio/Menu3.wav')
		self.switch_left.set_volume(0.8)
		self.switch_right=pygame.mixer.Sound('../assets/audio/Menu7.wav')
		self.switch_right.set_volume(0.8)
		self.menu_fix=pygame.mixer.Sound('../assets/audio/Menu12.wav')
		self.menu_fix.set_volume(0.8)

	def input(self):
		keys = pygame.key.get_pressed()

		if self.can_move:#一样设置时间间隔
			if keys[pygame.K_d] and self.selection_index < self.attribute_nr - 1:
				self.selection_index += 1
				self.switch_right.play()
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()
			elif keys[pygame.K_a] and self.selection_index >= 1:
				self.selection_index -= 1
				self.switch_left.play()
				self.can_move = False
				self.selection_time = pygame.time.get_ticks()

			if keys[pygame.K_SPACE]:
				self.can_move = False
				self.menu_fix.play()
				self.selection_time = pygame.time.get_ticks()
				self.item_list[self.selection_index].trigger(self.player)

	def selection_cooldown(self):#时钟
		if not self.can_move:
			current_time = pygame.time.get_ticks()
			if current_time - self.selection_time >= 300:
				self.can_move = True
	def create_items(self):
		self.item_list = []

		for item, index in enumerate(range(self.attribute_nr)):
			#水平位置上
			full_width = self.display_surface.get_size()[0]
			increment = full_width // self.attribute_nr
			left = (item * increment) + (increment - self.width) // 2
			
			# 竖直位置上
			top = self.display_surface.get_size()[1] * 0.1

			# 创建物品
			item = Item(left,top,self.width,self.height,index,self.font)
			self.item_list.append(item)

	def display(self):
		self.input()
		self.selection_cooldown()

		for index, item in enumerate(self.item_list):

			# get attributes
			name = self.attribute_names[index]
			value = self.player.get_value_by_index(index)
			max_value = self.max_values[index]
			cost = self.player.get_cost_by_index(index)
			item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item:
	def __init__(self,l,t,w,h,index,font):
		self.rect = pygame.Rect(l,t,w,h)
		self.index = index
		self.font = font

	def display_names(self,surface,name,cost,selected):
		color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

		# 标题
		title_surf = self.font.render(name,False,color)
		title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

		# 花费
		cost_surf = self.font.render(f'{int(cost)}',False,color)
		cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

		#绘画
		surface.blit(title_surf,title_rect)
		surface.blit(cost_surf,cost_rect)

	def display_bar(self,surface,value,max_value,selected):

		#画设置
		top = self.rect.midtop + pygame.math.Vector2(0,60)
		bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
		color = BAR_COLOR_SELECTED if selected else BAR_COLOR

		#设置
		full_height = bottom[1] - top[1]
		relative_number = (value / max_value) * full_height
		value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number,30,10)

		#画元素
		pygame.draw.line(surface,color,top,bottom,5)
		pygame.draw.rect(surface,color,value_rect)

	def trigger(self,player):#触发器
		upgrade_attribute = list(player.stats.keys())[self.index]

		if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
			player.exp -= player.upgrade_cost[upgrade_attribute]#扣除经验
			player.stats[upgrade_attribute] *= 1.2
			player.upgrade_cost[upgrade_attribute] *= 1.4

		if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
			player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]#最大值后不会再增加

	def display(self,surface,selection_num,name,value,max_value,cost):
		if self.index == selection_num:
			pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
		else:
			pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
			pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
	
		self.display_names(surface,name,cost,self.index == selection_num)
		self.display_bar(surface,value,max_value,self.index == selection_num)
#--------------游戏失败界面
def defeat_menu(window):
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
                    # window.fill((255,255,255))
                    # pygame.display.update()
                    return 1#代表重新开始
                elif quiet_key==1:#判断是否按到了退出游戏
                    pygame.quit()
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
    start_button=button(0,0,0,70,247,280,280,'START GAME',45,255,255,255)
    set_button=button(0,0,0,70,250,280,360,'STORY',45,255,255,255)
    quiet_button=button(0,0,0,70,250,300,440,'QUIT ',45,255,255,255)
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
                    return 5
                elif set_key==1:#判断是否按到了故事
                    window.fill((255,255,255))
                    pygame.display.update()
                    return 2
                elif quiet_key==1:#判断是否按到了退出游戏
                    return 9

#------------------以下是暂停界面
class stop_menu:
	def __init__(self,toggle_menu):
		# 常规设置
		self.toggle_menu = toggle_menu#用来执行是否关闭或打开界面
		self.display_surface = pygame.display.get_surface()#获取表面信息
		self.font = pygame.font.Font('../assets/font/DTM-Mono.otf', 30)#装载字体

		# 选项设置
		self.width = 400
		self.space = 10
		self.padding = 8

		item_inventory = {
			'CONTINUE':   0,
			'RESTART':  1,
			'QUIET': 2
			}
		self.item_inventory=item_inventory

		# 进入界面
		self.options = list(item_inventory.keys()) #一共有这么多行
		self.border = len(item_inventory) - 1
		self.setup()
		# 换行移动
		self.index = 0
		self.timer = Timer(200)
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
		# 选的文本画面
		self.choose_text =  self.font.render('choose',False,'Black')


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

				
				if self.index <= self.border:
					if self.item_inventory[current_item] ==0:
						self.toggle_menu()
						return 0
					elif self.item_inventory[current_item] ==1:
						self.toggle_menu()
						return 1
					elif self.item_inventory[current_item] ==2:
						pygame.quit()
						sys.exit()
		# 可以上下滚动保证不出界
		if self.index < 0:
			self.index = len(self.options) - 1
		if self.index > len(self.options) - 1:
			self.index = 0

	def show_entry(self, text_surf, top,selected):#展示画面

		# 背景
		bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

		# 文字
		text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20,bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)

		if selected:
			pygame.draw.rect(self.display_surface,'black',bg_rect,4,4)
			if self.index <= self.border: 
				pos_rect = self.choose_text.get_rect(midleft = (self.main_rect.left + 200,bg_rect.centery))
				self.display_surface.blit(self.choose_text,pos_rect)
		
	def update(self):
		restart_flag=self.input()

		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
			self.show_entry(text_surf, top,self.index == text_index)
		
		return restart_flag


class win_menu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()#获取表面信息
		self.image=pygame.image.load('../assets/photo/spr_mtebott_1.png')
		self.image=pygame.transform.scale(self.image,(800,600))
		self.font = pygame.font.Font('../assets/font/DTM-Mono.otf', 60)#装载字体
		self.text_surface = self.font.render('WIN', True, (255, 255, 255))  # 白色文本
		self.text_rect = self.text_surface.get_rect(center=(400, 150))
		self.quiet_button=button(0,0,0,100,200,300,500,'BACK',60,255,255,255)
	def draw(self):
		self.display_surface.fill((0, 0, 0))  #黑色背景
		self.display_surface.blit(self.image,(0,0))
		self.display_surface.blit(self.text_surface, self.text_rect)
		self.quiet_button.draw_button(self.display_surface)
		self.quiet_key=self.quiet_button.change_color(pygame.mouse.get_pos(),self.display_surface)
	def run(self):
		self.draw()
		self.mouse_buttons = pygame.mouse.get_pressed()
		if self.quiet_key == True:
			if self.mouse_buttons[0]:
				print(0)
				return 0
			else:
				return 4
		else:
			return 4
#________________到此为止------------------------------------------
