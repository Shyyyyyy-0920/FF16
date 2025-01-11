import pygame
class story:
    def __init__(self):
        self.image_files = [] 
        for i in range(17):
            self.image_files.append(f'../assets/story/{i}.png')
        self.images = [pygame.image.load(file).convert() for file in self.image_files]
        self.display_surface = pygame.display.get_surface()
        # 图片切换的时间间隔（秒）
        self.interval = 2000  # 1000 毫秒 = 1 秒
        # 当前显示的图片索引
        self.frame_index = 0
        self.use_time=0
    def get_time(self):
        if self.use_time == 0:
            self.start_time = pygame.time.get_ticks()
            self.use_time=1
        self.now_time=pygame.time.get_ticks()
        self.now_interval=self.now_time-self.start_time
    def draw(self):
        self.display_surface.fill('black')
        self.get_time()
        if self.now_interval>=self.interval:
            if self.frame_index >= 16:
                self.frame_index=16
            else:
                self.frame_index = self.frame_index+1
            self.start_time=pygame.time.get_ticks()
        self.display_surface.blit(self.images[self.frame_index], (0, 0))
        return 5