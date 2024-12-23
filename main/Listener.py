from add_event import add_event
#算是一个中间人，大概
DRAW = 1
STEP = 2
REQUEST_MOVE = 3
CAN_MOVE = 4

class Listener:  # 定义监听者类，该类可以响应事件以及发送新的事件
    def __init__(self,g_evene_queue:list): 
        self.g_evene_queue=g_evene_queue
    
    def post(self, event: str):
        add_event(event)
    
    def listen(self, event: str): 
        pass