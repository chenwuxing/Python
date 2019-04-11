class SingleNode:
    def __init__(self,elem):
        self.elem = elem
        self.next = None
    

class SingleLinkList:
    def __init__(self,node=None):
        # 私有属性头结点
        self.__head = node
    
    def length(self):
        count = 0
        cur = self.__head
        while cur != None:
            count += 1
            cur = cur.next
        return count
    
    def travel(self):
        cur = self.__head
        print('[',end=' ')
        while cur != None:
            print(cur.elem,end=' ')
            cur = cur.next
        print(']')

    def is_empty(self):
        return self.__head == None
    
    def add(self,item):
        node = SingleNode(item)
        node.next = self.__head
        self.__head = node
    
    def append(self,item):
        node = SingleNode(item)
        if self.is_empty():
            # 如果是空节点
            self.__head = node
        else:
            cur = self.__head
            while cur.next != None:
                cur = cur.next
            cur.next = node
    
    def insert(self,index,item):
        if index <= 0:
            self.add(item)
        elif index > (self.length() - 1):
            self.append(item)
        else:
            # 创建新结点
            node = SingleNode(item)
            # 遍历次数
            count = 0
            # 插入结点位置的上一个结点
            prev = self.__head
            # 查找到插入结点的上一个结点
            while count <  (index - 1):
                count += 1
                prev = prev.next
            # 新结点的下一个结点为上一个结点的下一个结点
            node.next = prev.next
            # 上一个结点的下一个结点为新的结点
            prev.next = node
    
    def remove(self,item):
        cur = self.__head
        pre = None
        found = False

        while not found:
            if cur.elem == item:
                found = True
            else:
                pre = cur
                cur = cur.next
        if pre == None:
            self.__head = self.__head.next
        else:
            pre.next = cur.next
    
    def search(self,item):
        cur = self.__head
        while cur != None:
            if cur.elem == item:
                return True
            else:
                cur = cur.next
        return False

if __name__ == '__main__':
    print('test:')
    single_link_list = SingleLinkList()

    print('--------判断是否为空-------')
    print(single_link_list.is_empty())

    print('-----------长度------------')
    print(single_link_list.length())

    single_link_list.append(2)
    single_link_list.append(3)
    single_link_list.append(5)

    print('-----------遍历------------')
    single_link_list.travel()

    single_link_list.add(1)
    single_link_list.add(0)
    single_link_list.insert(4, 4)
    single_link_list.insert(-1, -1)

    print('-----------遍历------------')
    single_link_list.travel()

    print('-----------查找------------')
    print(single_link_list.search(49))

    print('-----------删除------------')
    single_link_list.remove(-1)

    print('-----------遍历------------')
    single_link_list.travel()

    print('-----------长度------------')
    print(single_link_list.length())
        