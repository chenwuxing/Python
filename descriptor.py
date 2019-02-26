class Desc(object):

    def __get__(self, instance, owner):
        print("get!!!!")
        print("self=", self)
        print("instance=", instance)
        print("owner=", owner)
        print('*'*50, "\n")

    def __set__(self, instance, value):
        print("set!!!!")
        print("self=", self)
        print("instance=", instance)
        print("value=", value)
        print('*'*50, "\n")


class TestDesc(object):
    x = Desc()

t = TestDesc()
t.x

print(t.__dict__)
print(TestDesc.__dict__)
"""
t为实例，访问t.x时，顺序如下：
1.先访问实例属性，其次访问类属性
2.判断属性x为一个描述符，则将TestDesc.x转化为TestDesc.__dict__['x'].__get__(t,TestDesc)来访问
3.访问Desc的__get__()方法，进行相应的操作

"""



class Desc(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        print("get")
        print('name=',self.name) 
        print('*'*50, "\n")

class TestDesc(object):
    x = Desc('x')

    def __init__(self):
        self.y = Desc('y')

#以下为测试代码
t = TestDesc()
t.x
t.y

print(t.__dict__)
print(TestDesc.__dict__)
"""
obj.attr,obj是Myclass类型的
python中的属性查找顺序(考虑属性是描述符的情况)：
1.如果是python自己产生的属性，那么优先级是最高的，直接查找返回
2.如果Myclass.__getattribute__有定义则使用这个进行查找
3.如果attr是一个描述符对象，那么在Myclass.__dict__中查找，若查找到且attr是一个数据描述符则调用它的__get__方法，
  若查找不到按照Myclass.__mro__中的顺序在其父类__dict__中查找
4.在obj.__dict__中查找，若查找到直接返回属性，若查找不到进行下一步
5.在Myclass.__dict__中查找attr,若寻找到attr(必定是nondata_descriptor)则调用它的__get__方法
6.调用getattr方法

一般情况下若不涉及描述符，则实例属性查找的顺序是实例--->类--->父类--->直到元类(不包括元类)
若涉及描述符，则在实现细节上有所区别，分为obj和class两种情况
1.对于obj，obj.__getattribute__()将b.x转化为type(b).__dict__['x'].__get__(b,type(b))
2对于class,type.__getattribute()将B.x转化为B.__dict__['x'].__get__(None,B)
3.描述符被__getattribute__()方法掉用
4.覆盖__getattribute__()方法可以防止自动描述符调用
5.数据描述符将覆盖默认的属性查找链，改为自己的调用方法

-----------------------------------------------------------------------------------------------------
描述符：描述符是对象的一个属性，必须依附于对象存在，就和iterator一样，需要对象调用__iter__方法，存在于类的__dict__中，
并且定义有特殊方法，如__get__、__set__、__delete__

    类中的属性是对象，这个对象又是一个装饰器，那么对属性的查看和赋值实际是调用它的get和set方法


--------------------------------------------------------------------------------------------------------
关于python中属性的探究
1.属性的获取是按照从下到上的顺序来查找属性
2.类和实例是两个完全独立的对象
3.属性设置是针对对象本身进行的


"""


