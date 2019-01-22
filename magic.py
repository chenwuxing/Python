class Word(str):
    def __eq__(self,other):
        return len(self) == len(other)
w1 = Word('asd')
w2 = Word('xxx')
print('{} == {}?{}'.format(w1,w2,w1==w2))
print('asd==xxx? {}'.format('asd'=='xxx'))


# 重写new方法
class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(Singleton,cls).__new__(cls,*args,**args)
        return cls._instance

# str 、 repr
# 使用getattr 、setattr 、delattr可以随时修改删除添加属性或值
class Apple(object):
    def __init__(self,name,size):
        self.name = name
        self.size = size
    
    def __str__(self):
        return '{}:{}'.format(self.name,self.size)
    
    def __getattr__(self,key):
        # key = 60
        return key
    
    def __setattr__(self,name,value):
        self.__dict__[name] = ' {}'.format(value)


a=Apple('A','20g')
a.name = 'pig'
a.size = '200kg'
print('a.name:{} a.size:{}'.format(a.name,a.size))
print(a.age)

# 一个列表的封装类
# class FunctionalList:
#     def __init__(self,values=None):
#         if values is None:
#             self.values = []
#         # else:
#         #     self.values = values 这句有问题
    
#     def __len__(self):
#         return len(self.values)
    
#     def __getitem__(self,key):
#         return self.values[key]
    
#     def __setitem__(self,key,value):
#         self.values[key] = value
    
#     def __delitem__(self,key):
#         del self.values[key]
    
#     def __iter__(self):
#         return iter(self.values)
    
#     def __reversed__(self):
#         return reversed(self.values)
    
#     def append(self,value):
#         self.values.append(value)
    
#     def head(self):
#         return self.values[0]
    
#     def tail(self):
#         return self.values[1:]
    
#     def init(self):
#         return self.values[:-1]
    
#     def last(self):
#         return self.values[-1]
    
#     def drop(self,n):
#         return self.values[n:]
    
#     def take(self,n):
#         return self.values[:n]

# a = FunctionalList()
# print()
# a.append(5)
# print(a.head())

# 可调用的对象，call方法允许类的一个实例像函数那样被调用
# class Enitity:
#     def __init__(self,size,x,y):
#         self.x,self.y = x,y
#         self.size = size
    
#     def __call__(self,x,y):
#         self.x,self.y = x,y

# a = Enitity(1,22.5,56.5)
# print(a.x)
# a(30,40)
# print(a.x)

# pickle
# import pickle


# data = {'foo':[1,2,3],'bar':('hello','world!'),'baz':True}
# jar = open('data.pkl','wb')
# pickle.dump(data,jar)
# jar.close()
# pkl_file = open('data.pkl','rb')
# data = pickle.load(pkl_file)
# print(data)
# pkl_file.close()








