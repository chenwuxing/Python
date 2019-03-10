class Node:
    def __init__(self,init_data):
        self.data = init_data
        self.next = None
    
    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next
    
    def set_data(self,new_data):
        self.data = new_data
    
    def set_next(self,new_next):
        self.next = new_next
    

class Order_List:
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        return self.head == None
    
    def size(self):
        count = 0
        current_node = self.head
        while current_node != None:
            count += 1
            current_node = current_node.get_next()
    
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
        if previous == None():
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
    
    def search(self,element):
        current = self.head
        found  = False
        while not found and current != None:
            if current.get_data() == element:
                found  = True
            else:
                if current.get_data() > element:
                    print('所搜寻的值不在列表中')
                    break
                else:
                    current = current.get_next()
        return found
    
    def add(self,element):
        current = self.head
        previous = None
        stop = False
        while current != None and not stop:
            if current.get_data() > element:
                stop = True
            else:
                previous = current
                current = current.get_next()
        
        temp_node = Node(element)
        if previous == None:
            temp_node.set_next(current)
            self.head = temp_node
        else:
            temp_node.set_next(current)
            previous.set_next(temp_node)
    




