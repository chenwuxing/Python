class QueueNode:
    def __init__(self,data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self,node=None):
        self.__head = node
        self.__tail = node
        self.__tail = self.__head
        self.__count = 0
    
    def is_empty(self):
        return self.__head == None

    
    def length(self):
        return self.__count
    
    def enqueue(self,data):
    # 队尾入队
        node = QueueNode(data)
        if self.is_empty():
            self.__head = node
            self.__tail = node
            self.__count += 1
        else:
            self.__tail.next = node
            self.__tail = node
            self.__count += 1
    
    def dequeue(self):
        # 队头出队
        if self.is_empty():
            print('队列为空，操作违法')
        cur = self.__head
        self.__head = cur.next
        del cur
        self.__count -= 1
    
    def travel(self):
        cur  = self.__head
        print('[',end = '')
        while cur != None:
            print(cur.data,end=' ')
            cur = cur.next
        print(']',end = '')
    
if __name__ == '__main__':
    de = Queue()
    de.enqueue(1)
    de.enqueue(2)
    de.enqueue(3)
    print('-'*30 + '长度')
    print(de.length())
    print('-'*30 + '遍历')
    de.travel()
    de.dequeue()
    print('-'*30 + '遍历')
    de.travel()
    print('-'*30 + '长度')
    print(de.length())

    

        




