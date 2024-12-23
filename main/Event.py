class Event:  # 定义事件类，属性包括用于区分事件种类的编号，以及可选参数body传递一些信息
    def __init__(self, code: int, body={}):
        self.code = code
        self.body = body