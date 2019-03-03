from stack import Stack

def brackets_check(symbol_string):
    s = Stack()
    index = 0
    balance = True
    while index < len(symbol_string) and balance:
        if symbol_string[index] == "(":
            s.push(symbol_string[index])
        else:
            if s.is_empty():
                balance = False
            else:
                s.pop()
        index += 1

    if balance and s.is_empty():
        return True
    else:
        return False
print(brackets_check("((()))"))
print(brackets_check("((())))"))


