import pygame,sys
from openai import OpenAI
from typing import List, Dict
from chat_words import *
import judgement

# 初始化 OpenAI 客户端，连接到指定的服务器和 API 密钥
client = OpenAI(
    base_url='http://10.15.88.73:5002/v1',  # 指定 OpenAI API 的基础 URL
    api_key='ollama',  # API 密钥，这里设置为 'ollama'，但实际使用中可能需要有效的密钥
)

###！！！！！！！！！！！警告
###       以下内容过于屎山QAQ
###       会尽量用注释弥补的TAT

class ChatBot:
    def __init__(self, person , end = None):  #end 判定是否直接进入好结局对话，默认为None
        """
        初始化 ChatBox 类
        :param messages: 初始消息列表
        :param chat_history: 聊天历史记录列表
        """
        self.messages = [{}]  # 存储对话消息
        self.bg_color = (0,0,0)  # 设置背景颜色为黑色  
        self.screen = pygame.display.get_surface()# 读取屏幕状态   
        
        self.path = r"..\assets\font\DTM-Sans.otf"#字体文件路径
        self.font = pygame.font.Font(self.path, 20)  # 设置字体和大小为 20
        
        self.scroll_position = 0  # 鼠标滚动位置参数初始化
        
        self.output_text = ""  # 存储输出文本
        self.output_x = 10  # 输出文本的 x 坐标
        self.output_y = 10  # 输出文本的 y 坐标
        self.output_height = 400  # 输出文本区域的高度
        
        self.input_box = pygame.Rect(25, 475, 700, 32)  # 设置输入框的位置和大小
        self.color_inactive = pygame.Color(72,61,139)  # 输入框未激活时的颜色
        self.color_active = pygame.Color(255,255,255)  # 输入框激活时的颜色
        self.color = self.color_inactive  # 初始颜色为未激活颜色
        self.person = person  # 设置对话角色

        self.hint1 = "" #有关选项a的对话
        self.hint2 = "" #选项B的
        
        self.will_delta = 0 #善恶值的变化
        self.fight = None  #是否进入战斗
        self.anger = 0      #怒气值
        self.end = end     #判定结局

    def choose(person , end):#判断对话角色,联系上对应的类
        if person == "trader3":#第三关的trader
            name1 = trader3
            name2 = judgement.trader3
        
        elif person == "trader1":#第一关的trader
            name1 = trader1
            name2 = judgement.trader1
        
        elif person == "flowey":#精神状态格外美丽的小花（？
            name1 = monster2a
            name2 = judgement.monster_a
        
        elif person == "papyrus":#pap
            name1 = monster2b
            name2 = judgement.monster_a

        elif person == "temmie":#修勾勾（？
            name1 = monster2c
            name2 = judgement.monster_a

        elif person == "undyne":#undead鱼姐
            name1 = monster2d
            name2 = judgement.monster_a

        elif person == "sans0":   #sans对话1
            name1 = Sans0
            name2 = judgement.boss_a
        
        elif person == "sans1":
            name1 = Sans1
            name2 = judgement.boss_b  #sans对话2

        elif person == "sans2":
            name1 = Sans0
            name2 = judgement.boss_c   #sans对话3
        
        elif person == "sans3":   #结局对话
            if judgement.general.end == True  or \
                    end == True  or \
                    judgement.general.end == None  :#进入好结局的两种情况1. 按照流程走（内部程序判定） 2.累计善恶值(外部判定并传输）达到一定值，直接跳过中间过程，进入好结局
                name1 = Sans3
                name2 = judgement.boss_d
            else:
                name1 = Sans4
                name2 = judgement.boss_e

        else:
            name1 = None
            name2 = None
        return name1,name2

    def start(self,done,togggle_talk,get_pause_time=None,choose = choose):
        """
        根据聊天类型设置初始消息
        :return: 初始消息列表
        """
        start_time=pygame.time.get_ticks()
        screen = self.screen
        active = False  # 输入框是否激活
        text = ''  # 输入框中的文本
        chat_open = True  # 是否打开聊天界面

        name , name_a = choose(self.person , self.end)#与对应库的类建立联系

        self.messages = [
            {"role": "system", "content": name.quest},#设置对应的角色设定
            {"role": "user", "content": "Hello!"}
        ]

        image_chat = pygame.image.load(name.image).convert_alpha()#设置对应的角色图片
        image_chat=pygame.transform.scale(image_chat,(270,300))
        # image_chat = pygame.transform.scale(image_chat, (64, 64))

        if judgement.general.end == False:
            image_main = pygame.image.load(r"..\assets\chat\chara.png").convert_alpha()#猪脚变成Chara力（悲
            image_main = pygame.transform.scale(image_main, (80, 80))
        else:
            image_main = pygame.image.load(r"..\assets\graphics\player\down\down_0.png").convert_alpha()#猪脚图片
        # image_main = pygame.transform.scale(image_main, (64, 64))


        judgement_user = name_a.judge_user  #玩家对应输入内容的判定
        judgement_assistant = name_a.judge_assistant  #聊天对象对应的内容判定


        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # 如果事件类型是 QUIT，则结束循环
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        chat_open = not chat_open  # 按下 'Tab' 键退出聊天界面
                        done = False
                        togggle_talk()
                        if get_pause_time !=None:
                            end_time=pygame.time.get_ticks()
                            get_pause_time(start_time,end_time)
                        return self.will_delta , self.anger , self.fight   #返回最终的will_delta

#————————————————————————————————————————————正式开始聊天界面，输入框颜色变化“对焦与失焦”—————————————————————————————————— 
                if chat_open:
                    background_image = pygame.image.load(r"..\assets\chat\background1.png").convert_alpha()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.input_box.collidepoint(event.pos):
                            active = not active  # 如果点击输入框，则切换激活状态
                        else:
                            active = False  # 如果未点击输入框，则失活
                        self.color = self.color_active if active else self.color_inactive  # 更新输入框颜色

#————————————————————————————————————————输入对话讯息——————————————————————————————————————————————                   
                    
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                
                                self.hint1 , self.hint2 , inputa , chat_on= judgement_user(name_a,text)
                                
                                if chat_on == True:
                                    self.messages.append({"role": "user", "content": inputa})
                                    self.update_output(f"You: \n {inputa} \n ")
                                else:
                                    self.messages.append({"role": "user", "content": inputa +"  "+ text})  # 将用户输入添加到消息列表
                                    self.update_output(f"You: \n {inputa} \n {text} \n ")  # 更新输出文本
                                
                                try:
                                    response = client.chat.completions.create(
                                        model="llama3.2",
                                        messages=self.messages
                                    )
                                    assistant_reply = response.choices[0].message.content  # 获取助手回复
                                    
                                    outputa , will_delta , self.anger , self.fight= judgement_assistant(name_a,assistant_reply)
                                    
                                    if chat_on == True:
                                        self.update_output(f"{self.person}: \n {outputa} \n")  # 更新输出文本
                                        self.messages.append({"role": "assistant", "content": outputa})  # 将助手回复添加到消息列表
                                    else:
                                        self.update_output(f"{self.person}: \n {assistant_reply} \n {outputa} \n")  # 更新输出文本
                                        self.messages.append({"role": "assistant", "content": assistant_reply})  # 将助手回复添加到消息列表

                                    
                                    if will_delta != 0:                 # 对善恶值变化量的比较操作
                                        if  self.will_delta == will_delta:
                                            pass
                                        else:
                                            self.will_delta = will_delta
                                            

                                    
                                except Exception as e:
                                    self.update_output(f"Error: {e}")  # 处理异常并更新输出文本
                                    print(f"Error: {e}")
                                text = ''  # 清空输入框文本
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]  # 删除最后一个字符
                            else:
                                text += event.unicode  # 添加字符到输入框

# ——————————————————————————————————————————————————————输出框部分—————————————————————————
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:  # 鼠标滚轮向上滚动
                            self.scroll_position -= 20
                        elif event.button == 5:  # 鼠标滚轮向下滚动
                            self.scroll_position += 20
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.scroll_position -= 30  # 向上滚动
                        elif event.key == pygame.K_DOWN:
                            self.scroll_position += 30  # 向下滚动

#——————————————————————————————————————开渲！(?————————————————————————————————————————
            if chat_open:
                try:
                    screen.blit(background_image, (0, 0))  # 绘制背景图片
                except:
                    screen.fill(self.bg_color)  # 如果背景图片加载失败，则填充背景颜色

                txt_surface = self.font.render(text, True, self.color)  # 渲染输入框文本
                width = max(200, txt_surface.get_width()+10)  # 计算输入框宽度
                self.input_box.w = width  # 更新输入框宽度
                screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+2))  # 绘制输入框文本
                pygame.draw.rect(screen, self.color, self.input_box, 2)  # 绘制输入框边框
                pygame.draw.line(screen,(255,255,255), (550, 0), (550, 600), 5)
                pygame.draw.line(screen,(255,255,255), (550, 350), (800, 350), 5)
                pygame.draw.line(screen,(255,255,255), (0, 330), (550, 330), 5)
                self.render_output(screen)  # 渲染输出文本

                screen.blit(image_chat, (520, 0))  # 绘制角色
                screen.blit(image_main, (670, 490))

                int1 = self.font.render('Type 1 :',True,(72,61,139))  # 渲染提示文本
                int2 = self.font.render('Type 2 :',True,(72,61,139))
                Hint1 = self.font.render(self.hint1,True,(255,255,255))
                Hint2 = self.font.render(self.hint2,True,(255,255,255))
                hint_general1 = self.font.render("Use'yes'or'no nonsence' to quick-pass chating",True,(255,255,255))
                hint_general2 = self.font.render("Press the key 'TAB' to quit this chat",True,(255,255,255))
                screen.blit(int1,(20,345)) 
                screen.blit(int2,(20,405))
                screen.blit(Hint1,(15,375))
                screen.blit(Hint2,(15,430))
                screen.blit(hint_general1,(25,520))
                screen.blit(hint_general2,(25,555))
            
            
            else:
                break

            pygame.display.flip()  # 更新屏幕显示

    def update_output(self, message):
        """
        更新输出文本
        :param message: 要添加的消息
        """
        self.output_text += message + "\n"

    def render_output(self, screen):
        """
        在屏幕上渲染输出文本
        :param screen: pygame 屏幕对象
        """
        output_text = self.output_text
        output_x = 25
        output_y = 20
        output_height = 300
        font = self.font
        border_width = 500  # 边框宽度
        
        output_lines = output_text.split('\n')  # 将输出文本按换行符分割
        line_height = 24  # 每行的高度
        visible_lines = (output_height // line_height) + 1  # 可见行数

        # 计算初始垂直偏移量
        y_offset = -self.scroll_position

        processed_lines = []
        for line in output_lines:
            words = line.split()
            new_line = ""
            for word in words:
                test_line = new_line + " " + word if new_line else word
                if self.font.size(test_line)[0] > border_width:
                    processed_lines.append(new_line)
                    new_line = word
                else:
                    new_line = test_line
            if new_line:  # 确保不添加空行
                processed_lines.append(new_line)

        for i, line in enumerate(processed_lines):
            current_y = output_y + y_offset + i * line_height

            # 只绘制在可见区域内的行
            if 0 <= current_y < output_height:
                output_rendered_text = font.render(line, True, (255, 255, 255))  # 渲染每一行文本为图像
                screen.blit(output_rendered_text, (output_x + 10, current_y))  # 绘制文本到屏幕上

            # 如果已经超过了可见区域的最后一行，停止绘制
            if i >= visible_lines + self.scroll_position // line_height:
                break



