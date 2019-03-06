class Binary_tree:
    def __init__(self,root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None
    
    def insert_left(self,new_node):
        if self.left_child == None:
            self.left_child = Binary_tree(new_node)
        else:
            t = Binary_tree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self,new_node):
        if self.right == None:
            self.right_child = Binary_tree(new_node)
        else:
            t = Binary_tree(new_node)
            t.right_child = self.right_child
            self.right_child = t
    
    def get_left(self):
        return self.left_child
    
    def get_right(self):
        return self.right_child
    
    def get_root(self):
        return self.key
    
    def set_root(self,new_root_obj):
        self.key = new_root_obj
    



