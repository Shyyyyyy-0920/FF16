import pygame
from add_event import add_event,g_evene_queue
class story:
    def __init__(self):
        self.image_files = [] 
        for i in range(17):
            self.image_files.append(f'../assets/story/{i}.png')
        self.images = [pygame.image.load(file).convert() for file in self.image_files]
        self.display_surface = pygame.display.get_surface()
        # 图片切换的时间间隔（秒）
        self.interval = 1500  # 1000 毫秒 = 1 秒
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
        self.display_surface.blit(self.images[self.frame_index], (0, 0))
        if self.now_interval>=self.interval:
            if self.frame_index >= 16:
                self.frame_index=16
            else:
                self.frame_index = self.frame_index+1
            self.start_time=pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    add_event(0)
                elif event.key == pygame.K_ESCAPE:
                    add_event(0)
        if g_evene_queue[-1]==5:
            return 5
        elif g_evene_queue[-1]==0:
            return 0
#---------到此为止------------