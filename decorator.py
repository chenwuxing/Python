
import time

# # --------------------无参装饰器
def timmer(func):   #装饰器timmer,将函数foo的函数名为参数传给timmer
    def wrapper():
        start_time = time.time()
        func()
        stop_time = time.time()
        print('函数运行的时间是%s' %(stop_time-start_time))
    return wrapper

@timmer
def foo():
    time.sleep(2)
    print('正在学习装饰器')

# foo() #这里调用foo()其实就是指向了wrapper

#-------------------传参装饰器------------------------
def timmer1(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        stop_time = time.time()
        print('函数的运行时间是%s' %(stop_time-start_time))
    return wrapper

@timmer1
def my_max(x,y):
    time.sleep(3)
    res = x if x > y else y
    print('from the my_max,the max is %s' %res)

my_max(1,2)

# -----------------高阶函数定义
#   1.函数接收的参数是一个函数名 2.函数的返回值是一个函数名 3.满足上述条件任意一个，都可称之为高阶函数
def foo():
    print('我的函数名作为参数传递给高阶函数')
def high_order1(func):
    print('我就是高阶函数1，我接收的参数名是%s' %func)
def high_order2(func):
    print('我就是高阶函数2，我接收的参数名是%s' %func)

high_order1(foo)
high_order2(foo)


# ----------高阶函数应用1：把函数当做参数传给高阶函数
def student():
    print('我是一名学生')

def timmer2(func):
    start_time = time.time()
    func()
    stop_time = time.time()
    print('函数%s运行时间是%s' %(func,stop_time-start_time))
timmer2(student)

# --------缺点是虽然可以给函数增加功能，但是已经改变了函数的执行方式
"""
1.函数接收的参数是一个函数名
    作用：在不修改函数源代码的前提下，为函数添加新功能
    缺点：会改变函数的调用方式

2.函数的返回值是一个函数名
    作用：不修改函数的调用方式
    缺点：没啥卵用

"""

# --------------函数嵌套---------------------
def father(name):
    print('from father %s' %name)
    def son():
        print('from son')
        def grandson():
            print('from grandson')
        grandson()
    son()
 
father('chenwuxing')

# ---------------------闭包-------------------------
"""
这里outer函数的返回值是一个内部的函数对象inner,这里inner用到了x这个引用变量
这里的closure=outer(1)，closure这个变量成为inner函数对象的引用，那么closure()就等于inner()
closure就是一个闭包
"""
def outer(x):
    def inner():
        print(x)
    return inner
closure = outer(1)
closure()












