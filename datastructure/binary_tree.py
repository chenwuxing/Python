class BTNode:
    def __init__(self,data= None):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:

    def __init__(self,init_list):
        self.init_list = init_list
        self.root = self.create(self.init_list)

    def create(self,node_list):
        # 列表中的第一个元素用来创建根节点，如果根节点为None，那树就是空树
        if node_list[0] == None:
            return None
        head = BTNode(node_list[0])
        # 将创建的树节点放入一个列表中
        Nodes = [head]
        # 第一个元素已经用来创建根节点了
        j = 1
        for node in Nodes:
            if node != None:
                # 如果节点存在，并且列表中元素不等于None，那么为其创建左孩子节点
                node.left = (BTNode(node_list[j]) if node_list[j] != None else None)
                # 节点列表添加新创建的节点
                Nodes.append(node.left)
                # 列表元素向后移一位
                j += 1
                # 判断j是否越界
                if j == len(node_list):
                    return head
                # 如果节点存在，并且列表中元素不等于None，那么为其创建右孩子节点
                node.right = (BTNode(node_list[j]) if node_list[j] != None else None)
                Nodes.append(node.right)
                j += 1
                if j == len(node_list):
                    return head
    
    def preorder_traverse(self,head):
        if head == None:
            return
        print(head.data,end = ' ')
        self.preorder_traverse(head.left)
        self.preorder_traverse(head.right)
    
    def inorder_traverse(self,head):
        if head == None:
            return 
        self.inorder_traverse(head.left)
        print(head.data,end = ' ')
        self.inorder_traverse(head.right)
    
    def postorder_traverse(self,head):
        if head == None:
            return 
        self.postorder_traverse(head.left)
        self.postorder_traverse(head.right)
        print(head.data,end = ' ')




if __name__ == '__main__':
    bt = BinaryTree([1,2,3,4,5,None,6,None,None,7,8])
    print('-'*30 + '先序遍历' + '-'*30)
    bt.preorder_traverse(bt.root)
    print('\n')
    print('-'*30 + '中序遍历' + '-'*30)
    bt.inorder_traverse(bt.root)
    print('\n')
    print('-'*30 + '后序遍历' + '-'*30)
    bt.postorder_traverse(bt.root)


        
                







