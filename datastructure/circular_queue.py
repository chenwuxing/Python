class CircularQueue:
    '''
    常规顺序存储结构队列存在的问题
    1.入队操作性能很好，可以做到o(1)时间复杂度，但是出队操作的时间复杂度为o(n)，
    2.如果限制了队列的大小，那么便会出现’假溢出’的现象
    '''
    def __init__(self,max_size,node = None):
        self.__head = 0
        self.__tail = 0
        self.__data = [None]*max_size
        self.__maxsize = max_size
    
    def length(self):
        # 通用的计算队列长度
        return (self.__tail - self.__head + self.__maxsize) % self.__maxsize
    
    def enqueue(self,data):
        # 队列满的判断
        if (self.__tail + 1) % self.__maxsize == self.__head:
            print('队列已满，操作违法')
            return False
        self.__data[self.__tail] = data
        self.__tail = (self.__tail + 1) % self.__maxsize
    
    def dequeue(self):
        if self.__head == self.__tail:
            print('队列为空，操作违法')
            return False
        self.__data[self.__head] = None
        self.__head = (self.__head + 1) % self.__maxsize
    
    def travel(self):
        print(self.__data)
    
if __name__ == '__main__':
    cq = CircularQueue(10)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    cq.enqueue(4)
    print(cq.length())
    cq.travel()
    cq.dequeue()
    cq.travel()





