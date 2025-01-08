import pygame
from openai import OpenAI
from typing import List, Dict
from chat_words import *

# 初始化 OpenAI 客户端，连接到指定的服务器和 API 密钥
client = OpenAI(
    base_url='http://10.15.88.73:5002/v1',  # 指定 OpenAI API 的基础 URL
    api_key='ollama',  # API 密钥，这里设置为 'ollama'，但实际使用中可能需要有效的密钥
)

# 临时设定参数，用户初始拥有的金钱数量
user_money = 200

# 初始化字体模块
pygame.font.init()

class ChatBox_Trader:
    def __init__(self, messages: List[Dict] = [{}], chat_history: List[Dict] = []):
        """
        初始化 ChatBox 类
        :param messages: 初始消息列表
        :param chat_history: 聊天历史记录列表
        """
        self.messages = messages  # 存储对话消息
        self.chat_history = chat_history  # 存储聊天历史记录
        self.bg_color = (200, 200, 200)  # 设置背景颜色为浅灰色
        self.font = pygame.font.Font(None, 24)  # 设置字体和大小为 24
        self.output_text = ""  # 存储输出文本
        self.scroll_position = 0  # 滚动位置
        self.output_x = 10  # 输出文本的 x 坐标
        self.output_y = 10  # 输出文本的 y 坐标
        self.output_height = 400  # 输出文本区域的高度

    def chat(self, chat_type, screen):
        """
        处理聊天逻辑
        :param chat_type: 聊天类型，可以是 "trader" 或 "player"
        :param screen: pygame 屏幕对象
        """
        self.messages = self.initial_message(chat_type)
        input_box = pygame.Rect(30, 500, 700, 32)  # 设置输入框的位置和大小
        color_inactive = pygame.Color(0, 0, 0)  # 输入框未激活时的颜色
        color_active = pygame.Color('dodgerblue2')  # 输入框激活时的颜色
        color = color_inactive  # 初始颜色为未激活颜色
        active = False  # 输入框是否激活
        text = ''  # 输入框中的文本
        done = False  # 是否结束循环
        chat_open = True  # 是否打开聊天界面

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True  # 如果事件类型是 QUIT，则结束循环
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        chat_open = not chat_open  # 按下 'Tab' 键切换聊天界面
                if chat_open:
                    self.handle_events(event, input_box, active, text, color, screen)
                    self.handle_input(event, active, text, chat_type)
                    self.handle_mouse(event, input_box, active, color)
                    self.handle_scroll(event)

            if chat_open:
                self.draw_screen(screen, input_box, color, text)
            else:
                break

            pygame.display.flip()  # 更新屏幕显示

        pygame.quit()  # 退出 pygame

    def initial_message(self, chat_type):
        """
        根据聊天类型设置初始消息
        :param chat_type: 聊天类型，可以是 "trader" 或 "player"
        :return: 初始消息列表
        """
        if chat_type == "trader":
            return [
                {"role": "system", "content": }
            ]
        elif chat_type == "player":
            return [
                {"role": "system", "content": "We are going to play a game now, and I have an integer in my mind. "
                                             "You can ask me an integer each time, and I will tell you whether the answer "
                                             "will be larger or smaller than the number asked. "
                                             "You need to use the minimum number of questions to answer what the answer is. "
                                             "For example, when the answer in my mind is 200, you can ask 100 and I will "
                                             "tell you that the answer is greater than 100."}
            ]
        return []

    def handle_events(self, event, input_box, active, text, color, screen):
        """
        处理事件
        :param event: pygame 事件
        :param input_box: 输入框 Rect 对象
        :param active: 输入框是否激活
        :param text: 输入框中的文本
        :param color: 输入框颜色
        :param screen: pygame 屏幕对象
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active  # 如果点击输入框，则切换激活状态
            else:
                active = False  # 如果未点击输入框，则失活
            color = self.color_active if active else self.color_inactive  # 更新输入框颜色
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 鼠标滚轮向上滚动
                self.scroll_position -= 30
            elif event.button == 5:  # 鼠标滚轮向下滚动
                self.scroll_position += 30

    def handle_input(self, event, active, text, chat_type):
        """
        处理输入
        :param event: pygame 事件
        :param active: 输入框是否激活
        :param text: 输入框中的文本
        :param chat_type: 聊天类型，可以是 "trader" 或 "player"
        """
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    self.messages.append({"role": "user", "content": text})  # 将用户输入添加到消息列表
                    self.update_output(f"User: {text}")  # 更新输出文本
                    try:
                        response = client.chat.completions.create(
                            model="llama3.2",
                            messages=self.messages
                        )
                        assistant_reply = response.choices[0].message.content  # 获取助手回复
                        self.update_output(f"Llama: {assistant_reply}")  # 更新输出文本
                        self.messages.append({"role": "assistant", "content": assistant_reply})  # 将助手回复添加到消息列表
                        self.chat_history.append({"user": text, "ai": assistant_reply})  # 更新聊天历史记录
                        if chat_type == "trader":
                            self.judgement_user(text)  # 如果是交易模式，则判断用户输入
                    except Exception as e:
                        self.update_output(f"Error: {e}")  # 处理异常并更新输出文本
                    text = ''  # 清空输入框文本
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]  # 删除最后一个字符
                else:
                    text += event.unicode  # 添加字符到输入框
            if event.key == pygame.K_UP:
                self.scroll_position -= 30  # 向上滚动
            elif event.key == pygame.K_DOWN:
                self.scroll_position += 30  # 向下滚动

    def handle_mouse(self, event, input_box, active, color):
        """
        处理鼠标事件
        :param event: pygame 事件
        :param input_box: 输入框 Rect 对象
        :param active: 输入框是否激活
        :param color: 输入框颜色
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active  # 如果点击输入框，则切换激活状态
            else:
                active = False  # 如果未点击输入框，则失活
            color = self.color_active if active else self.color_inactive  # 更新输入框颜色

    def handle_scroll(self, event):
        """
        处理滚动事件
        :param event: pygame 事件
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 鼠标滚轮向上滚动
                self.scroll_position -= 30
            elif event.button == 5:  # 鼠标滚轮向下滚动
                self.scroll_position += 30

    def draw_screen(self, screen, input_box, color, text):
        """
        绘制屏幕
        :param screen: pygame 屏幕对象
        :param input_box: 输入框 Rect 对象
        :param color: 输入框颜色
        :param text: 输入框中的文本
        """
        self.background_image = pygame.image.load("background2.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (800, 600))
        if self.background_image:
            screen.blit(self.background_image, (0, 0))  # 绘制背景图片
        else:
            screen.fill(self.bg_color)  # 如果背景图片加载失败，则填充背景颜色

        txt_surface = self.font.render(text, True, color)  # 渲染输入框文本
        width = max(200, txt_surface.get_width() + 10)  # 计算输入框宽度
        input_box.w = width  # 更新输入框宽度
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  # 绘制输入框文本
        pygame.draw.rect(screen, color, input_box, 2)  # 绘制输入框边框

        self.render_output(screen)  # 渲染输出文本

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
        output_lines = self.output_text.split('\n')  # 将输出文本按换行符分割
        y_offset = 10 - self.scroll_position  # 计算初始垂直偏移量
        for line in output_lines:
            output_rendered_text = self.font.render(line, True, (0, 0, 0))  # 渲染每一行文本为图像
            if self.output_y + y_offset + 30 > self.output_y and self.output_y + y_offset < self.output_y + self.output_height:
                screen.blit(output_rendered_text, (self.output_x + 10, self.output_y + y_offset))  # 绘制文本到屏幕上
            y_offset += 30  # 增加垂直偏移量

    def judgement_user(self, user_input):
        """
        判断用户的购买或出售操作
        :param user_input: 用户输入的字符串
        """
        global user_money
        if not user_input:
            self.update_output("Do you still want to buy something?")
            return

        words = user_input.lower().split()
        if len(words) != 3:
            self.when_come_to_wrong_words()
            return

        action, goods, quantity_str = words
        quantity = int(quantity_str) if quantity_str.isdigit() else 0

        if action == "buy":
            price = self.value(goods, "buy")
            if price == 0:
                self.when_come_to_wrong_words()
            elif price * quantity > user_money:
                self.update_output(f"You don't have enough money! Now you have {user_money} dollars!")
            else:
                user_money -= price * quantity
                self.update_output(f"You have bought {quantity} {goods}! Now you have {user_money} dollars!")
        elif action == "sell":
            price = self.value(goods, "sell")
            if price == 0:
                self.when_come_to_wrong_words()
            else:
                user_money += price * quantity
                self.update_output(f"You have sold {quantity} {goods}! Now you have {user_money} dollars!")
        else:
            self.when_come_to_wrong_words()

    def value(self, goods_name, condition):
        """
        获取商品的价格
        :param goods_name: 商品名称
        :param condition: 操作类型，可以是 "buy" 或 "sell"
        :return: 商品价格
        """
        if condition == "buy":
            return {
                "corn": 4,
                "tomato": 5,
                "apple_vision_s_pro_max_ultra_turbo_plus": 29999
            }.get(goods_name, 0)
        elif condition == "sell":
            return {
                "corn": 10,
                "tomato": 20,
                "apple": 2,
                "wood": 4
            }.get(goods_name, 0)
        return 0

    def when_come_to_wrong_words(self):
        """
        处理用户输入错误的情况
        """
        self.update_output("We can't identify your words! Please check your input lines~")

# 创建并运行TraderChat实例
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    trader_chat = ChatBox_Trader()
    trader_chat.chat("trader", screen)
