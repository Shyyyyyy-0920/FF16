g_evene_queue = []  # 事件队列
def add_event(event):  # 向事件队列中添加事件
    global g_evene_queue
    g_evene_queue.append(event)
    return g_evene_queue
#--------到此为止-------