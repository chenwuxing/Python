from stack import Stack

def d2b(input_num):
    """
    功能：将十进制数转换为二进制数
    参数
        input_num:输入的十进制数
    返回值：对应字符串类型的二进制数
    """
    s= Stack()
    symbol = True
    quotient,remainder = divmod(input_num,2)
    while symbol:
        if not quotient == 0:
            s.push(remainder)
            next_quotient,next_remainder = divmod(quotient,2)
            quotient,remainder = next_quotient,next_remainder
        else:
            s.push(remainder)
            symbol = False
    
    size = s.size()
    result = ''
    for i in range(size):
        pop_element = s.pop()
        result  = result + str(pop_element)
    return result

print(d2b(168))








