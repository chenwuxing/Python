class DoubleNode:
    def __init__(self,elem):
        self.elem = elem
        self.pre = None
        self.next = None


class DoubleLinkList:
    '''
    非循环双向链表，所以第一个节点的pre为None,最后一个结点的next为None
    '''
    def __init__(self,node=None):
        # 私有属性头结点
        self.__head = node
    
    def is_empty(self):
        return self.__head == None
    
    def length(self):
        count = 0
        cur = self.__head
        while cur != None:
            count += 1
            cur = cur.next
        return count
    
    def travel(self):
        cur = self.__head
        print('[',end = ' ')
        while cur != None:
            print(cur.elem,end = ' ')
            cur = cur.next
        print(']')
    
    # 链表头部添加元素
    def add(self,item):
        node = DoubleNode(item)
        # 新结点的下一个结点为旧链表的头结点
        node.next = self.__head
        # 新链表的头结点为新结点
        self.__head = node
        # 下一个结点的上一个结点指向新增的节点
        node.next.pre = node
    
    # append(item) 链表尾部添加元素
    def append(self,item):
        node = DoubleNode(item)
        if self.is_empty():
            # 为空节点时
            self.__head = node
        else:
            # 让指针指向最后节点
            cur = self.__head
            while cur.next != None:
                cur = cur.next
            # 最后节点的下一个为新添加的node
            cur.next = node
            # 新添加的节点上一个结点是当前结点
            node.pre = cur
    

    # search(item)查找结点是否存在
    def search(self,item):
        # 当前节点
        cur = self.__head
        while cur != None:
            if cur.elem == item:
                return True
            else:
                cur = cur.next
        return False
    
    def insert(self,index,item):
        if index <= 0:
            self.add(item)
        elif index > (self.length() - 1):
            self.append(item)
        else:
            # 创建新节点
            node = DoubleNode(item)
            cur = self.__head
            # 遍历次数
            count = 0
            # 查找到插入结点的上一个结点
            while count < index:
                count += 1
                cur = cur.next

            # 新结点的下一个结点指向当前节点
            node.next = cur
            # 新结点的上一个结点指向当前节点的上一个结点
            node.pre = cur.pre
            # 当前节点的上一个结点的下一个结点指向新结点
            cur.pre.next = node
            # 当前节点的上一个结点指向新结点
            cur.pre = node
    
    # remove(item)删除结点
    def remove(self,item):
        cur = self.__head
        while cur != None:
            if cur.elem == item:
                '''
                当前节点的值等于目标值，若要删除当前目标
                分为3种情况
                1.当前结点是第一个节点
                    1>当前链表中只有一个结点
                    2>当前链表中结点数量大于1，将第一个节点的下一个结点的前驱指针设置为None
                2.当前节点是中间节点
                3.当前节点是最后一个结点
                '''
                if cur == self.__head:
                    # 头结点
                    self.__head = cur.next
                    if cur.next:
                        # 如果不是只有一个结点
                        cur.next.pre = None
                else:
                    #当前节点的上一个结点的下一个指向当前节点的下一个结点
                    cur.pre.next = cur.next
                    # 如果当前节点不是尾节点
                    if cur.next:
                        # 当前节点的下一个结点的上一个结点指向当前节点的上一个结点
                        cur.next.pre = cur.pre
                return # 返回当前节点
            
            # 没找到，向后移
            else:
                cur = cur.next


if __name__ == '__main__':
    print('test:')
    double_link_list = DoubleLinkList()

    print('--------判断是否为空-------')
    print(double_link_list.is_empty())

    print('-----------长度------------')
    print(double_link_list.length())

    double_link_list.append(2)
    double_link_list.append(3)
    double_link_list.append(5)

    print('-----------遍历------------')
    double_link_list.travel()

    double_link_list.add(1)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.add(0)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.insert(4, 4)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.insert(-1, -1)

    print('-----------遍历------------')
    double_link_list.travel()

    print('-----------查找------------')
    print(double_link_list.search(4))

    print('-----------删除------------')
    double_link_list.remove(5)
    double_link_list.remove(-1)

    print('-----------遍历------------')
    double_link_list.travel()

    print('-----------长度------------')
    print(double_link_list.length())


    
    
