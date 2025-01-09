import pygame

class chat_general:
        user_money = 200 #测试用金币额度
        humanity_point = 6  #善恶值

class chat_input:
        color_inactive = pygame.Color(0,0,0)  # 输入框未激活时的颜色
        color_active = pygame.Color('dodgerblue2')  # 输入框激活时的颜色
        input_box = pygame.Rect(30, 500, 700, 32)  # 设置输入框的位置和大小

class chat_output:
        color = pygame.Color(0,0,0)  #输出框的颜色
        output_x = 10  # 输出文本的 x 坐标
        output_y = 10  # 输出文本的 y 坐标
        output_height = 400  # 输出文本区域的高度

