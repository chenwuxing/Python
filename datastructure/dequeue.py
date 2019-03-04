class Deque():
    """
    双向队列：一种特殊的线性表，在表头和表尾均可添加或删除元素
    主要操作：
        add_front:在表头插入element元素
        add_rear:在表尾插入element元素
        remove_front:从表头使第一个元素出队，并返回其值
        remove_rear：从表尾使第一个元素出队，并返回其值
        is_empty:判断双向队列是否为空
        size:返回双向队列的长度
        """
    def __init__(self):
        self.item = []

    def add_front(self,element):
        self.item.insert(0,element)

    def add_rear(self,element):
        self.item.append(element)

    def remove_front(self):
        return self.item.pop(0)

    def remove_rear(self):
        return self.item.pop()

    def is_empty(self):
        return self.item == []

    def size(self):
        return len(self.item)





