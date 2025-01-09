import pygame
from openai import OpenAI
from typing import List, Dict
from chat_words import *

# 初始化 OpenAI 客户端，连接到指定的服务器和 API 密钥
client = OpenAI(
    base_url='http://10.15.88.73:5002/v1',  # 指定 OpenAI API 的基础 URL
    api_key='ollama',  # API 密钥，这里设置为 'ollama'，但实际使用中可能需要有效的密钥
)



class ChatBot:
    def __init__(self, person):
        """
        初始化 ChatBox 类
        :param messages: 初始消息列表
        :param chat_history: 聊天历史记录列表
        """
        self.messages = [{}]  # 存储对话消息
        self.chat_history = []  # 存储聊天历史记录
        self.bg_color = (0,0,0)  # 设置背景颜色为浅灰色    
        self.screen = pygame.display.get_surface()# 屏幕对象   
        self.path = r"..\assets\font\DTM-Sans.otf"


        self.font = pygame.font.Font(self.path, 22)  # 设置字体和大小为 22
        
        self.scroll_position = 0  # 滚动位置
        
        self.output_text = ""  # 存储输出文本
        self.output_x = 10  # 输出文本的 x 坐标
        self.output_y = 10  # 输出文本的 y 坐标
        self.output_height = 400  # 输出文本区域的高度
        
        self.input_box = pygame.Rect(30, 500, 700, 32)  # 设置输入框的位置和大小
        self.color_inactive = pygame.Color(72,61,139)  # 输入框未激活时的颜色
        self.color_active = pygame.Color(255,255,255)  # 输入框激活时的颜色
        self.color = self.color_inactive  # 初始颜色为未激活颜色
        self.person = person  # 设置对话角色


    def start(self):
        """
        根据聊天类型设置初始消息
        :return: 初始消息列表
        """
        person = self.person
        screen = self.screen
        active = False  # 输入框是否激活
        text = ''  # 输入框中的文本
        done = False  # 是否结束循环
        chat_open = True  # 是否打开聊天界面

        if person == "trader3":
            name = trader3
        if person == "trader1":
            name = trader1
        if person == "flowey":
            name= monster2a

        self.messages = [
            {"role": "system", "content": name.quest},#设置对应的角色设定
            {"role": "user", "content": "Hello!"}
        ]

        image_chat = pygame.image.load(name.image).convert_alpha()
        image_chat=pygame.transform.scale(image_chat,(270,300))
        # image_chat = pygame.transform.scale(image_chat, (64, 64))

        image_main = pygame.image.load(r"..\assets\graphics\player\down\down_0.png").convert_alpha()
        # image_main = pygame.transform.scale(image_main, (64, 64))


        '''judgement_user = Judgement.name.judgement_user'''#暂时不用


        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # 如果事件类型是 QUIT，则结束循环
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        chat_open = not chat_open  # 按下 'Tab' 键退出聊天界面
                        done = True

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
                                self.messages.append({"role": "user", "content": text})  # 将用户输入添加到消息列表
                                self.update_output(f"Frisk: {text}")  # 更新输出文本
                                
                                try:
                                    response = client.chat.completions.create(
                                        model="llama3.2",
                                        messages=self.messages
                                    )
                                    assistant_reply = response.choices[0].message.content  # 获取助手回复
                                    self.update_output(f"{self.person}: {assistant_reply}")  # 更新输出文本
                                    
                                    self.messages.append({"role": "assistant", "content": assistant_reply})  # 将助手回复添加到消息列表
                                    self.chat_history.append({"user": text, "ai": assistant_reply})  # 更新聊天历史记录
                                    # judgement_user(text)  # 如果是交易模式，则判断用户输入
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
            else:
                break

            pygame.display.flip()  # 更新屏幕显示

        pygame.quit()  # 退出 pygame

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
        output_x = 40
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



