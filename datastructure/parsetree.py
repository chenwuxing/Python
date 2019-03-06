from stack import Stack
from tree import Binary_tree

def build_parse_tree(fpexp):
    fplist = fpexp.split()
    p_stack = Stack()
    e_tree = Binary_tree('')
    p_stack.push(e_tree)
    current_tree = e_tree
    for i in fplist:
        if i == '(':
            current_tree.insert_left('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_left()
        
        elif i not in ['+','-','*','/',')']:
            current_tree.set_root(int(i))
            parent = p_stack.pop()
            current_tree = parent
        
        elif i in ['+','-','*','/']:
            current_tree.set_root(i)
            current_tree.insert_right('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_right()
        
        elif i == ')':
            current_tree = p_stack.pop()
        else:
            raise ValueError
        
    return e_tree

def evalutate(parse_tree):
    operation = {'+':operator.add,'-':operator.sub,'*':operator.mul,'/':operator.truediv}
    left_child = parse_tree.get_left()
    right_child = parse_tree.get_right()

    if left_child and right_child:
        func_operation = operation[parse_tree.get_root()]
        return func_operation(evalutate(left_child),evalutate(right_child))
    else:
        return parse_tree.get_root()
