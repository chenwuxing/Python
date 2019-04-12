class StackNode:
    def __init__(self,data=None):
        self.data = data
        self.next = None
    

class LinKStack:
    def __init__(self,node=None):
        self.__head = node
        self.count = 0
    
    def length(self):
        return self.count

    def push(self,data):
        node = StackNode(data)
        node.next = self.__head
        self.__head = node
        self.count += 1
    
    def pop(self):
        if self.length() == 0:
            print('栈为空，操作不合法')
            return False
        else:
            cur = self.__head
            self.__head = cur.next
            del cur
            self.count -= 1
    
    def travel(self):
        cur = self.__head
        print('[',end = '')
        while cur != None:
            print(cur.data,end=' ')
            cur = cur.next
        print(']',end = '')
    
if __name__ == '__main__':
    ls = LinKStack()
    ls.push(1)
    ls.push(2)
    ls.push(3)
    print('-'*30 + '遍历' + '-'*30)
    ls.travel()
    ls.pop()
    print('-'*30 + '遍历' + '-'*30)
    ls.travel()
    ls.push(666)
    print('-'*30 + '遍历' + '-'*30)
    ls.travel()
    




    