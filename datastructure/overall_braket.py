from stack import Stack

def brackets_check(symbol_string):
    s = Stack()
    index = 0
    balance = True
    while index < len(symbol_string) and balance:
        if symbol_string[index] in "{([":
            s.push(symbol_string[index])
        else:
            if s.is_empty():
                balance = False
                break
            else:
                stack_top_element = s.pop()
                # 如果栈顶元素与其不匹配，那么即可认为是错误的括号书写
                if not match(stack_top_element,symbol_string[index]):
                    balance = False
                    break
        index += 1

    if balance and s.is_empty():
        return True
    else:
        return False



def match(open,close):
    open_string = "{(["
    close_string = "})]"
    return open_string.index(open) == close_string.index(close)


print(brackets_check("[{()}]"))
print(brackets_check("[{][]"))



