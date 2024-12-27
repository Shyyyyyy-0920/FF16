#这里是按钮类
import pygame

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