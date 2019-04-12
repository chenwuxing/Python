class SingleNode:
    def __init__(self,elem):
        self.elem = elem
        self.next = None
    

class SingleCircleLinkList:
    # 私有属性头结点
    def __init__(self,node=None):
        # 私有属性头结点
        self.__head = node
# -------------------- 这部分可以有，也可以没有，功能是增加一个头结点----------------------------------------------
        if node:
            # 不是构造空的链表
            # 头结点的下一个结点指向头结点
            node.next = node
    
    def is_empty(self):
        return self.__head == None
    
    def length(self):
        if self.is_empty():
            return 0

        count = 1
        # 当前节点
        cur = self.__head
        # 当前节点的下一个结点不是头结点则继续增加
        while cur.next != self.__head:
            count += 1
            # 当前节点往后移
            cur = cur.next
        return count
    

    def travel(self):
        # 访问的当前节点
        if self.is_empty():
            return False
        
        cur = self.__head
        print('[',end = ' ')
        while cur.next != self.__head:
            print(cur.elem,end = ' ')
            cur = cur.next
        print(cur.elem,end=' ')
        print(']')
    

    # add(item) 链表头部添加元素
    def add(self,item):
        node = SingleNode(item)
        if self.is_empty():
            # 空链表
            self.__head = node
            node.next = node
        else:
            # 非空链表增加
            cur = self.__head
            # 查找最后一个结点
            while cur.next != self.__head:
                cur = cur.next
            # 新结点的下一个结点为旧链表的头结点
            node.next = self.__head
            # 新链表的头结点为新结点
            self.__head = node
            # 最后结点的下一个结点指向新结点
            cur.next = node

    # 链表尾部添加元素
    def append(self,item):
        node = SingleNode(item)
        if self.is_empty():
            # 为空节点时
            self.__head = node
            node.next = node
        else:
            # 让指针指向最后节点
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            # 最后节点的下一个结点为新添加的Node
            cur.next = node
            node.next = self.__head
    
    #insert(index,item)指定位置(从0开始)添加元素
    def insert(self,index,item):
        if index <= 0:
            # 在前方插入
            self.add(item)
        elif index > (self.length() - 1):
            # 在最后添加
            self.append(item)
        else:
            # 创建结点
            node = SingleNode(item)
            # 遍历次数
            count = 0
            # 插入结点位置的上一个结点
            pre = self.__head
            # 查找到插入结点的上一个结点
            while count < (index - 1):
                count += 1
                pre = pre.next
            # 新结点的下一个结点为上一个结点的下一个结点
            node.next = pre.next
            # 上一个结点的下一个结点为新的结点
            pre.next = node
    
    def remove(self,item):
        if self.is_empty():
            return False
        cur = self.__head
        pre = None

        while cur.next != self.__head:
            # 找到符合条件的目标
            if cur.elem == item:
                '''
                此时会有3种情况
                1.目标是第一个节点
                2.目标是中间结点
                3.目标是尾节点
                '''
                # 目标是第一个节点
                if cur == self.__head:
                    # 删除节点，先找尾节点
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    # 头结点指向当前节点的下一个结点
                    self.__head = cur.next
                    rear.next = self.__head
                else:
                    # 中间结点，上一个结点的下一个结点指向当前节点的下一个结点
                    pre.next = cur.next
                return #返回当前节点
            else:
                # 没找到，向后移
                pre = cur
                cur = cur.next
        
        # 循环结束cur指向尾节点
        if cur.elem == item:
            if pre:
                # 如果删除最后一个结点
                pre.next = cur.next
            else:
                # 删除只含有一个结点的链表的第一个节点
                self.__head = None
        

    def search(self,item):
        cur = self.__head
        while cur.next != self.__head:
            if cur.elem == item:
                return True
            else:
                cur = cur.next
        # 判断最后一个元素
        if cur.elem == item:
            return True
        return False



if __name__ == '__main__':
    print('test:')
    single_circle_link_list = SingleCircleLinkList()

    print('--------判断是否为空-------')
    print(single_circle_link_list.is_empty())

    print('-----------长度------------')
    print(single_circle_link_list.length())

    single_circle_link_list.append(2)
    single_circle_link_list.append(3)
    single_circle_link_list.append(5)
    #
    print('-----------遍历------------')
    single_circle_link_list.travel()
    #
    single_circle_link_list.add(1)
    single_circle_link_list.add(0)
    single_circle_link_list.insert(4, 4)
    single_circle_link_list.insert(-1, -1)
    #
    print('-----------遍历------------')
    single_circle_link_list.travel()
    #
    print('-----------查找------------')
    print(single_circle_link_list.search(4))
    #
    print('-----------删除------------')
    single_circle_link_list.remove(4)

    print('-----------遍历------------')
    single_circle_link_list.travel()

    print('-----------长度------------')
    print(single_circle_link_list.length())







