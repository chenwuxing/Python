def dec1(func):
    print('我是装饰器1，打印我')
    def wrapper1():
        print('111111')
        return func()
    return wrapper1

def dec2(func):
    print('我是装饰器2，打印我')
    def wrapper2():
        print('222222222')
        return func()
    return wrapper2
@dec2
@dec1
def foo():
    print('我是一个傻子')

foo()

"""
装饰器只对函数进行修饰，不修饰装饰器
1.dec1先修饰foo函数，相当于执行foo = dec1(foo)，所以打印'我是装饰器1，打印我',foo指向wrapper1
2.dec1装饰完foo函数后，dec2修饰foo，相当于执行foo = dec2(wrapper1),所以打印'我是装饰器2，打印我',foo指向wrapper2
3.执行foo()就相当于执行wrapper2(),所以打印'222222222',然后执行到return func()，此时的func是
   wrapper1(),所以打印'111111',再执行到return func(),此时的func才是最初的foo函数，所以打印
   我是一个傻子
"""

