
# 类方法的实例
class ClassTest(object):
    _num = 0

    @classmethod
    def add_num(cls):
        cls._num += 1

    @classmethod
    def get_num(cls):
        return cls._num
    
    def __new__(self):
        ClassTest.add_num()
        return super(ClassTest,self).__new__(self)
    

class Student(ClassTest):
    def __init(self):
        self.name = ''

a = Student()
b = Student()
print(ClassTest.get_num())
