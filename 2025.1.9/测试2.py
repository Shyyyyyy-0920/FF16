import pygame

def render_output(self, screen, output_text):
    """
    在屏幕上渲染输出文本
    :param screen: pygame 屏幕对象
    """
    output_text = output_text
    output_x = 20
    output_y = 20
    output_height = 300
    font = font
    scroll_position = scroll_position
    border_width =5  # 边框宽度
    
    output_lines = output_text.split('\n')  # 将输出文本按换行符分割
    line_height = 20  # 每行的高度
    visible_lines = (output_height // line_height) + 1  # 可见行数

    # 计算初始垂直偏移量
    y_offset = -scroll_position

    processed_lines = []
    for line in output_lines:
        words = line.split()
        new_line = ""
        for word in words:
            test_line = new_line + " " + word if new_line else word
            if self.font.size(test_line)[0] > self.border_width:
                processed_lines.append(new_line)
                new_line = word
            else:
                new_line = test_line
        processed_lines.append(new_line)

    # 处理连词符
    final_lines = []
    for i in range(len(processed_lines)):
        if i > 0:
            last_char = processed_lines[i-1][-1]
            first_char = processed_lines[i][0]
            if last_char.isalpha() and first_char.isalpha():
                final_lines.append(processed_lines[i-1] + "-" + processed_lines[i])
            else:
                final_lines.append(processed_lines[i-1])
                final_lines.append(processed_lines[i])
        elif i == 0:
            final_lines.append(processed_lines[i])

    for i, line in enumerate(final_lines):
        current_y = self.output_y + y_offset + i * line_height

        # 只绘制在可见区域内的行
        if 0 <= current_y < self.output_height:
            output_rendered_text = self.font.render(line, True, (0, 0, 0))  # 渲染每一行文本为图像
            screen.blit(output_rendered_text, (self.output_x + 10, current_y))  # 绘制文本到屏幕上

        # 如果已经超过了可见区域的最后一行，停止绘制
        if i >= visible_lines + self.scroll_position // line_height:
            break