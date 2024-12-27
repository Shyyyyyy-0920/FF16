import pygame
import sys
import random
FPS=60
BLACK=(0,0,0)
WHITE=(255,255,255)
clock=pygame.time.Clock()
pygame.init()
window_lenth=800#窗口初始长度
window_height=600#窗口初始宽度
#创建游戏窗口
window=pygame.display.set_mode((window_lenth,window_height))
#C设置游戏标题
pygame.display.set_caption('真相之下')
 #设置游戏背景颜色
window.fill(BLACK)
line_start_lst=[0,200]
line_end_lst=[800,200]
pygame.display.flip()
class my_heart(pygame.sprite.Sprite):
    HP=100
    def __init__(self,line_start_lst,line_end_lst):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('arrests/Image/heart.png')
        
        self.rect=self.image.get_rect()
        self.rect.center = (window_lenth/2,window_height/2)
        self.rect.bottom= window_height-3
        self.line_start_lst=line_start_lst
        self.line_end_lst=line_end_lst
    def update(self):
        
        key_pressd=pygame.key.get_pressed()
        if key_pressd[pygame.K_d]:
            self.rect.x+=6
        if key_pressd[pygame.K_a]:
            self.rect.x-=6
        if key_pressd[pygame.K_w]:
            self.rect.y-=6
        if key_pressd[pygame.K_s]:
            self.rect.y+=6
        if self.rect.right >=self.line_end_lst[0]:
            self.rect.right=self.line_end_lst[0]
        if self.rect.left<=self.line_start_lst[0]:
            self.rect.left=self.line_start_lst[0]
        if self.rect.bottom>=window_height:
            self.rect.bottom=window_height
        if self.rect.top<=self.line_start_lst[1]:
            self.rect.top=self.line_start_lst[1]

class bullet(pygame.sprite.Sprite):
    def __init__(self,line_start_lst,line_end_lst):
        self.line_start_lst=line_start_lst
        self.line_end_lst=line_end_lst
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('arrests/Image/B_DOWN_w.png')
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(self.line_start_lst[0],self.line_end_lst[0]-self.rect.width)
        self.rect.y=self.line_end_lst[1]
        self.speedy=random.randrange(2,10)
        self.speedx=random.randrange(-3,3)
    def update(self):
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx
        if self.rect.top > window_height or self.rect.left > self.line_end_lst[0]or self.rect.right <self.line_start_lst[0]:
            self.rect.x=random.randrange(self.line_start_lst[0],self.line_end_lst[0]-self.rect.width)
            self.rect.y=self.line_end_lst[1]
            self.speedy=random.randrange(4,12)
            self.speedx=random.randrange(-4,4)
def battle(line_start_lst,line_end_lst):
    line_start=tuple(line_start_lst)
    line_end=tuple(line_end_lst)
    myhp=my_heart.HP#用于记录战斗时的血量
    all_sprites=pygame.sprite.Group()
    bullets=pygame.sprite.Group()
    player = my_heart(line_start_lst,line_end_lst)
    all_sprites.add(player)
    for i in range(8):
        b=bullet(line_start_lst,line_end_lst)
        all_sprites.add(b)
        bullets.add(b)

    while 1:
        clock.tick(FPS)
        #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        all_sprites.update()
        #判断是否发生碰撞
        hits=pygame.sprite.spritecollide(player,bullets,False)
        if hits:
            myhp=myhp-1
            if myhp<=0:
                return 3
        #用于显示血量 
        title_HP=str(myhp)
        window.fill(BLACK)
        show_hp=button(0,0,0,30,30,660,550,title_HP,30,255,255,255)
        show_hp.draw_button(window)
        
        
        boss_image=pygame.image.load('arrests/人物/demon/idle1.png')
        window.blit(boss_image,(line_end_lst[0]/2,line_start_lst[1]-200))
        all_sprites.draw(window)
        pygame.draw.line(window,(255,255,255),line_start,line_end)
        pygame.display.update()
    pygame.quit()




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
        font=pygame.font.Font('arrests/write_style/DTM-Mono.otf',self.size)
        pygame.draw.rect(window,(self.r1,self.g1,self.b1),(self.inix,self.iniy,self.width,self.height))#绘制矩形
        text=font.render(self.text,True,(self.r2,self.g2,self.b2))
        tw1,th1=text.get_size()
        tx1=self.inix+self.width/2-tw1/2
        ty1=self.iniy+self.height/2-th1/2
        window.blit(text,(tx1,ty1))
        pygame.display.update()
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


#这里是之前写的失败界面

WHITE=(255,255,255)
def lose(window):
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('arrests/Image/结束界面背景.jpg')
    # 渲染图片
    window.blit(image1,(0,0))
    pygame.display.update()
    restart_button=button.button(255,255,255,70,350,240,60,'RESTART GAME',45,0,0,0)
    quiet_button=button.button(255,255,255,70,250,300,440,'QUIET ',45,0,0,0)
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
                    return 2
                elif quiet_key==1:#判断是否按到了退出游戏
                    sys.exit()


#这里是之前写的菜单界面
WHITE=(255,255,255)
def menu(window):
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('arrests/photo/background_menu.png')
    # 渲染图片
    window.blit(image1,(0,0))
    pygame.display.update()
    start_button=button.button(0,0,0,70,247,280,280,'start game',45,255,255,255)
    set_button=button.button(0,0,0,70,250,280,360,'set',45,255,255,255)
    quiet_button=button.button(0,0,0,70,250,300,440,'QUIET ',45,255,255,255)
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
                    return 2
                elif set_key==1:#判断是否按到了设置
                    window.fill((255,255,255))
                    pygame.display.update()
                    return 4
                elif quiet_key==1:#判断是否按到了退出游戏
                    sys.exit()


##---------------------------这里是对stop界面的要求
#这个主要实现做一个游玩过程中暂停的界面，界面只需要有继续游戏，重新开始，返回菜单和退出游戏这四个按钮（我写了按钮类，不需要考虑按钮如何写）
# 玩家鼠标点击暂停按钮会弹出暂停的界面，不会将游玩画面覆盖，同时游戏时间变为0，只是在原来的画面上进行绘制，点继续开始将会
# （第一个选择是删除之前绘画的所有暂停界面的按钮，同时游戏重新开始运行，这样就可以回到游玩界面，第二个是重新绘制暂停前的画面，然后游戏继续）

#难点是如何做到在战斗过程中实现暂停和继续，因为飞机和子弹一直在运动，如果觉得困难可以先不实现在战斗中暂停

def stop():

    #第一个按钮，继续游戏
    continue_button=button()

    #第二个按钮，重新开始
    restart_button=button()#我上面写了button需要传入的参数

    #第三个按钮，返回菜单
    back_menu_button=button()

    #第四G个按钮，退出游戏
    quiet_button=button()

    #创建完按钮写出对应的事件，再做判断
    #注意命名规范与注释的必要
#________________------------------------------------------



#--------之前写的一些关于地图的用法-------------------------------------------------------------------
def move(key_pressd,rect_x,rect_y):
    key_pressd=pygame.key.get_pressed()
    if key_pressd[pygame.K_d]:
        rect_x+=6
    elif key_pressd[pygame.K_a]:
        rect_x-=6
    elif key_pressd[pygame.K_w]:
        rect_y-=6
    elif key_pressd[pygame.K_s]:
        rect_y+=6

def darw_map():
    window.fill(WHITE)
    #加载图片
    image1=pygame.image.load('arrests/photo/地图.png')
    # 渲染图片
    window.blit(image1,(0,0))
#------实现动画效果-----------------

    key_pressd=pygame.key.get_pressed()
    if key_pressd[pygame.K_w]: 
        frames_me_forward=[]
        for i in range(1,3):
            frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
            frame=pygame.transform.scale(frame,(50,50))
            frames_me_forward.append(frame) 
        rect=frame.get_rect()
        rect.y-=6
        window.fill(WHITE)
        window.blit(frames_me_forward[index],(100,100))
        pygame.display.update()
        index=(index+1)%len(frames_me)
        clock.tick(FPS)
        
    if key_pressd[pygame.K_s]: 
        frames_me_down=[]
        for i in range(3,5):
            frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
            frame=pygame.transform.scale(frame,(50,50))
            frames_me_down.append(frame) 
        rect=frame.get_rect()
        rect.y+=6
        window.fill(WHITE)
        window.blit(frames_me_forward[index],(100,100))

    if key_pressd[pygame.K_d]: 
        frames_me_right=[]
        for i in range(5,7):
            frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
            frame=pygame.transform.scale(frame,(50,50))
            frames_me_right.append(frame) 
        rect=frame.get_rect()
        rect.x+=6
        window.fill(WHITE)
        window.blit(frames_me_forward[index],(100,100))
    
    if key_pressd[pygame.K_a]: 
        frames_me_left=[]
        for i in range(7,9):
            frame=pygame.image.load(f'arrests/人物/勇者系列人物/{i}.png')
            frame=pygame.transform.scale(frame,(50,50))
            frames_me_left.append(frame)
        rect=frame.get_rect()
        rect.x-=6
        window.fill(WHITE)
        window.blit(frames_me_forward[index],(100,100))
    
#--------设置帧率------------------
    clock = pygame.time.Clock()
    index = 0
    pygame.display.update()
    while 1:
    #检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        window.fill(WHITE)
        window.blit(frames_me_forward[index],(100,100))
        #-----更新屏幕---------
        
    pygame.quit()


#-----------------------------------------------------------------------------------

#这里写所有角色最基本的类，这个类需要有这几个参数1.这个角色的样子（会放在文件夹里，可以直接读取）2.这个角色的HP3.这个角色相遇时说的话
#一些特殊角色，比如主角与敌人，需要有特殊的类，可以用类继承普通人的类再扩充，主角有自己技能，有自己的装备，有自己的动图，敌人有动图和自己的技能

#--------主角--------
image_role_path=[0,0,0,0,0,0,0,0]
image_role_path[0]='arrests/人物/勇者系列人物/1.png'
image_role_path[1]='arrests/人物/勇者系列人物/2.png'
image_role_path[2]='arrests/人物/勇者系列人物/3.png'
image_role_path[3]='arrests/人物/勇者系列人物/4.png'
image_role_path[4]='arrests/人物/勇者系列人物/5.png'
image_role_path[5]='arrests/人物/勇者系列人物/6.png'
image_role_path[6]='arrests/人物/勇者系列人物/7.png'
image_role_path[7]='arrests/人物/勇者系列人物/8.png'
#--------主角--------
#--------敌人--------
image_enemy1_path='arrests/人物/demon/idle1.png'
image_enemy2_path='arrests/人物/demon/idle2.png'
image_enemy3_path='arrests/人物/demon/idle3.png'
image_enemy4_path='arrests/人物/demon/idle4.png'
image_enemy5_path='arrests/人物/demon/idle5.png'
image_enemy6_path='arrests/人物/demon/idle6.png'
image_enemy7_path='arrests/人物/demon/idle7.png'
image_enemy8_path='arrests/人物/demon/idle8.png'
#--------敌人--------
#--------npc---------
image_npc1_path='arrests/人物/ixangling/imgdon1.png'
image_npc2_path='arrests/人物/ixangling/imgdon2.png'
image_npc3_path='arrests/人物/ixangling/imgdon3.png'
image_npc4_path='arrests/人物/ixangling/imgdon4.png'
image_npc5_path='arrests/人物/ixangling/imgdon5.png'
image_npc6_path='arrests/人物/ixangling/imgdon6.png'
image_npc7_path='arrests/人物/ixangling/imgdon7.png'
image_npc8_path='arrests/人物/ixangling/imgdon8.png'
image_npc9_path='arrests/人物/ixangling/imgdon9.png'
image_npc10_path='arrests/人物/ixangling/imgdon10.png'
image_npc11_path='arrests/人物/ixangling/imgdon11.png'
image_npc12_path='arrests/人物/ixangling/imgdon12.png'
image_npc13_path='arrests/人物/ixangling/imgdon13.png'
image_npc14_path='arrests/人物/ixangling/imgdon14.png'
image_npc15_path='arrests/人物/ixangling/imgdon15.png'
image_npc16_path='arrests/人物/ixangling/imgdon16.png'
#--------npc---------
#--------小怪--------
image_ghost1_path='arrests/Image/Animation/ghost1.png'
image_ghost2_path='arrests/Image/Animation/ghost2.png'
image_ghost3_path='arrests/Image/Animation/ghost3.png'
image_ghost4_path='arrests/Image/Animation/ghost4.png'
image_ghost5_path='arrests/Image/Animation/ghost5.png'
image_ghost6_path='arrests/Image/Animation/ghost6.png'
image_ghost7_path='arrests/Image/Animation/ghost7.png'
#--------小怪--------


#注意命名规范与注释的必要
class people:

    def __init__(self,image_path:str,people_hp:int,people_title:str):
        #要读取人物模型矩形框的长宽以及坐标
        self.image_path=image_path
        self.people_hp=people_hp
        self.people_title=people_title
    

    def say(self):
        #这里要画个图形，底色为白色，中间显示要说的话，只有一句，为英文，显示在人物上方
        pass



#----------主角和敌人的先不写---------
class role(people):#这是主角的类，继承普通人
    def __init__(self):
        pass

class enemy(people):#这是主角的类，继承普通人
    def __init__(self):
        pass
