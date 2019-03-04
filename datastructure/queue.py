class Queue():
    """
    队列：一个特殊的线性表，先进先出，类似于生活中的排队
    主要操作：
        enqueue:参数是入队元素，无返回值，队列改变
        dequeue；从队列头返回并删除首元素
        is_empty:判断队列是否为空，如果为空，那么返回True，否则返回False
        size:返回队列的长度
    """
    def __init__(self):
        self.item = []
        
    def enqueue(self,element):
        self.item.append(element)

    def dequeue(self):
        return self.item.pop(0)

    def is_empty(self):
        return self.item == []

    def size(self):
        return len(self.item)




        
    