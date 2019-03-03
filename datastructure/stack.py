"""
栈被构造为项的有序集合，特点是后进先出
操作如下：
1.Stack()创建一个空栈，不需要参数，并返回一个空栈
2.push(element)将一个新项添加到栈的顶部，并不返回任何内容
3.pop()从栈中删除栈顶元素，栈被修改
4.peek()从栈返回顶部元素
5.is_empty()测试栈是否为空栈
6.size()返回栈找那个的元素数量
"""
class Stack():
    def __init__(self):
        self.item = []
    
    def push(self,element):
        self.item.append(element)
    
    def pop(self):
        return self.item.pop(-1)
    
    def peek(self):
        return (self.item[-1])
    
    def is_empty(self):
        return self.item == []
    
    def size(self):
        return len(self.item)



s = Stack()
s.is_empty()
s.push(4)
s.push('dog')
s.peek()
s.push(True)
print(s.size())
print(s.is_empty())
s.push(8.4)
print(s.pop())
print(s.pop())
print(s.size())





