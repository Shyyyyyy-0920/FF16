from Listener import Listener
import pygame
pygame.init()  # 初始化pygame
g_window = pygame.display.set_mode((1000, 800))  # 窗口大小

DRAW = 1
STEP = 2
REQUEST_MOVE = 3
CAN_MOVE = 4
class EntityLike(Listener):  # 实体类
    def __init__(self, image: pygame.Surface, rect: pygame.Rect):
        # 两个属性代表显示的图片路径、显示的矩形的位置和大小
        self.image = image
        self.rect = rect

    def listen(self, event):
        if event.code == DRAW:
            g_window.blit(self.image, self.rect)
    def draw(self, camera: tuple[int, int]):  # 定义显示实体的方法，该方法在场景需要描绘图像的时候调用
        rect = self.rect.move( *(-i for i in camera))  
        # 根据摄像头的位置计算实际要描绘的位置，例如摄像头往上了，实际描绘的位置就要往下
        # 实际上就是将该实体的横纵坐标分别减去摄像头左上角的坐标
        # 这里move方法是产生了一个新的rect，而不是修改了原有的rect。例如，障碍物墙体原本的位置应该是在生成以后就不变的
        # 对于玩家来说，玩家往一个方向移动之后，在这里描绘时又会被向相反方向移动，因此表现出玩家在镜头中间不动的效果
        g_window.blit(self.image, rect)  # 调用pygame的方法描绘图像