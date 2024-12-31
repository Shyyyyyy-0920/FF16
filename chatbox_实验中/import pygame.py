import pygame
import sys

# 初始化pygame
pygame.init()

# 初始化字体模块
pygame.font.init()

class ChatBox:
    def __init__(self, screen, font, output_x, output_y, output_width, output_height, input_x, input_y, input_width, \
                 input_height):
        self.screen = screen
        self.font = font
        self.output_x = output_x
        self.output_y = output_y
        self.output_width = output_width
        self.output_height = output_height
        self.output_color = (253, 255, 208)

        self.input_x = input_x
        self.input_y = input_y
        self.input_width = input_width
        self.input_height = input_height
        self.input_color = (200, 200, 200)  # 浅灰色背景

        self.output_text = ""
        self.input_text = ""
        self.scroll_position = 0
        self.scroll_step = 30  # 每次滚动的步长

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # 将输入内容添加到输出文本
                    self.output_text += self.input_text + "\n"
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # 鼠标滚轮向上滚动
                    self.scroll_position = max(0, self.scroll_position - self.scroll_step)
                elif event.button == 5:  # 鼠标滚轮向下滚动
                    self.scroll_position += self.scroll_step

    def draw(self):
        # 绘制输出对话框背景
        pygame.draw.rect(self.screen, self.output_color, (self.output_x, self.output_y, self.output_width, self.output_height), 0)
        
        # 绘制输出对话框内容
        output_lines = self.output_text.split('\n')
        y_offset = 10 - self.scroll_position
        for line in output_lines:
            output_rendered_text = self.font.render(line, True, (0, 0, 0))  # 黑色文字
            if self.output_y + y_offset + 30 > self.output_y and self.output_y + y_offset < self.output_y + self.output_height:
                self.screen.blit(output_rendered_text, (self.output_x + 10, self.output_y + y_offset))
            y_offset += 30

        # 绘制输入对话框背景
        pygame.draw.rect(self.screen, self.input_color, (self.input_x, self.input_y, self.input_width, self.input_height), 0)
        
        # 绘制输入对话框内容
        input_rendered_text = self.font.render(self.input_text, True, (0, 0, 0))  # 黑色文字
        self.screen.blit(input_rendered_text, (self.input_x + 10, self.input_y + 10))

        # 绘制“聊天内容”文字
        chat_label = self.font.render("Chating", True, (0, 0, 0))  # 黑色文字
        self.screen.blit(chat_label, (self.output_x - chat_label.get_width() - 10, self.output_y + (self.output_height // 2) - (chat_label.get_height() // 2)))

        # 绘制“输入”文字
        input_label = self.font.render("Input", True, (0, 0, 0))  # 黑色文字
        self.screen.blit(input_label, (self.input_x - input_label.get_width() - 10, self.input_y + (self.input_height // 2) - (input_label.get_height() // 2)))


class Game:
    def __init__(self, screen_width, screen_height, background_image_path):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("对话框示例")
        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        self.chat_box = ChatBox(self.screen, self.font,
                                output_x=(screen_width - 600) // 2, output_y=50, output_width=600, output_height=400,
                                input_x=(screen_width - 500) // 2, input_y=500, input_width=500, input_height=5)

    def run(self):
        running = True
        while running:
            self.chat_box.handle_events()
            self.screen.blit(self.background_image, (0, 0))  # 绘制背景图
            self.chat_box.draw()  # 绘制对话框
            pygame.display.flip()


# 设置屏幕大小
screen_width, screen_height = 800, 600

# 创建游戏实例
game = Game(screen_width, screen_height, "dialog_bg.png")

# 运行游戏
game.run()