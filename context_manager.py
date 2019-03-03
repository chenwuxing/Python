"""
一个对象只要实现了__enter__()和__exit__()方法，那么它就是一个
上下文管理器，上下文管理器可以使用with关键字
"""

class File():
    def __init__(self,filename,mode):
        self.filename = filename
        self.mode = mode
    
    def __enter__(self):
        print("entering")
        self.f = open(self.filename,self.mode)
        return self.f

    def __exit__(self,*args):
        print("will exit")
        self.f.close()
    
with File('C:/Users/wuxing/Desktop/清华源.txt','a') as f:
    print('writting')
    f.write('实现了一个上下文管理器')


"""
contextlib中提供了一个contextmanager的装饰器，通过yield将函数分割成两部分
yield之前的语句在__enter__方法中执行，yield之后的语句在__exit__方法中执行
yield关键字之后的值是函数的返回值
"""
from contextlib import contextmanager

@contextmanager
def my_open(path,mode):
    f = open(path,mode)
    yield f 
    f.close()

with my_open('C:/Users/wuxing/Desktop/清华源.txt','a') as f:
    f.write('this is a context manager')



