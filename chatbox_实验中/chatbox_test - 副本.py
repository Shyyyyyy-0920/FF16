import pygame
import sys,os, string


class inputbox:
    def __init__(self,surf,left,top,width,height,font):
        self.surf = surf
        self.font = font
        self.rect = pygame.Rect(left,top,width,height)
        self.list = []
        #是否激活
        self.active = False
        #是否绘制光标
        self.cursor = True
        #是否绘制计数器
        self.count = 0
        #此刻是否删除(按下删除键后变成True)
        self.delete = False


    def draw(self):
        # 画框
        pygame.draw.rect(self.surf, (0, 0, 0), self.rect, 1)
        
        # 投放文字
        text_pic = self.font.render(''.join(self.list), True, (0, 0, 0))
        text_rect = text_pic.get_rect(midleft=self.rect.midleft)
        text_rect.x += 5
        self.surf.blit(text_pic, text_rect)

        # 实时更新光标计数器，判断是否换行
        self.count += 1
        if self.count == 20:
            self.count = 0
            self.cursor = not self.cursor

        # 绘制光标
        if self.active and self.cursor:
            # 计算光标的位置
            cursor_x = text_rect.x + text_pic.get_width() + 5
            pygame.draw.line(self.surf, (255, 255, 255), 
                             (cursor_x, self.rect.y + 5), 
                             (cursor_x, self.rect.y + self.rect.height - 5), 1)

        # 删除文字功能
        if self.delete and self.list:
            self.list.pop()
    

    def get_text(self,event):#输入内容
        if event.type == pygame.MOUSEBUTTONDOWN:#有关鼠标的操作
            if self.rect.collidepoint(event.pos):
                self.active = True#按到文本框，开始编辑
            else:
                self.active = False#按到其他地方，光标消失

        elif self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:#删除键
                    self.delete = True
                elif event.unicode in string.ascii_letters or \
                    event.unicode in "0123456789_":#键盘输入的字符
                    self.list.append(event.unicode)
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:#删除键弹回就不删除字符
                    self.delete = False

    @property
    def text(self):#获取内容
        return ''.join(self.list)
                



# demo  一般测试用  代码

if __name__ == '__main__':
    # 设置工作路径
    import os

# 获取chatbox_test.py所在的目录路径（即桌面路径）
    path = os.path.dirname("c:\\Users\\VehicleZero\\Desktop\\chatbox_test.py")#不太懂文件设置，先这样吧
    os.chdir(path)
    # 基本设置 
    pygame.init()
    screen = pygame.display.set_mode((1000,800))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)
    
    # 创建两张文字图片
    image1 = font.render('User ID',True,(0,0,0))
    image2 = font.render('Password',True,(0,0,0))
    
    # 创建文本框
    account = inputbox(screen,270,100,300,40,font)
    password = inputbox(screen,270,200,300,40,font)

    while True:
        clock.tick(60)#绘制内容
        screen.fill((255,255,255))    
        screen.blit(image1,(150,110))
        screen.blit(image2,(150,220))
        account.draw()
        password.draw()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                account.get_text(event)
                password.get_text(event)
                if event.type == pygame.KEYDOWN:   
                    if event.key == pygame.K_RETURN:
                        print(account.text,password.text)#测试用，打印输入内容


        pygame.display.update()

    
    # input_box = inputbox(screen,100,100,400,30,font)
