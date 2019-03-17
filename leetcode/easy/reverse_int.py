class Solution:
    
    def reverse(self, x):
        if x < 0:
            y = -1*int(str(-x)[::-1])
        else:
            y = int(str(x)[::-1])
        if y > 2147483647 or y < -2147483648:
            y = 0
        return y
"""
知识点：切片[start:end:step]，当step = -1时代表反向
整数不支持逆序切片，先把整数转为字符串，然后逆序切片
当字符串形如'00012',int()函数可以使其变为12，忽略前面的0
"""