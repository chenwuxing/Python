"""
List():创建一个新的空列表。它不需要参数，并返回一个空列表。
add(item):向列表中添加一个新项。它需要 item 作为参数，并不返回任何内容。假定该 item 不在列表中。
remove(item):从列表中删除该项。它需要 item 作为参数并修改列表。假设项存在于列表中。
search(item):搜索列表中的项目。它需要 item 作为参数，并返回一个布尔值。
isEmpty():检查列表是否为空。它不需要参数，并返回布尔值。
size():返回列表中的项数。它不需要参数，并返回一个整数。
append(item):将一个新项添加到列表的末尾，使其成为集合中的最后一项。它需要 item 作为参数，并不返回任何内容。假定该项不在列表中。
index(item):返回项在列表中的位置。它需要 item 作为参数并返回索引。假定该项在列表中。
insert(pos，item):在位置 pos 处向列表中添加一个新项。它需要 item 作为参数并不返回任何内容。假设该项不在列表中，并且有足够的现有项使其有 pos 的位置。
pop():删除并返回列表中的最后一个项。假设该列表至少有一个项。
pop(pos):删除并返回位置 pos 处的项。它需要 pos 作为参数并返回项。假定该项在列表中。

"""

class Node:

    def __init__(self,init_data):
        self.data = init_data
        self.next = None
    
    def get_data(self):
        return self.data
    
    def set_data(self,new_data):
        self.data = new_data
    
    def get_next(self):
        return self.next
    
    def set_next(self,new_next):
        self.next = new_next

class Unordered_list:
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        return self.head == None
    
    def add(self,element):
        tmp = Node(element)
        tmp.set_next(self.head)
        self.head = tmp
    
    def size(self):
        current_node = self.head
        count = 0
        if self.head == None:
            return 0
        else:
            while current_node != None:
                count += 1
                current = current.get_next()
            return count + 1
    
    def search(self,element):
        current_node = self.head
        found  = False
        while current_node != None and not found:
            if current_node.get_data() == element:
                found  = True
            else:
                current_node = current_node.get_next()
            
        return found 
    
    def remove(self,element):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.get_data() == element:
                found = True
            else:
                previous = current
                current = current.get_next()
        if previous == None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    
    






    


