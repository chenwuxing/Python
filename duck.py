class duck():
    def walk(self):
        print('duck is walking')
    def swim(self):
        print('duck is swimming')

class person():
    def walk(self):
        print('this person walking like duck')
    def swim(self):
        print('this person is swimming')

def test_game(obj):
    obj.walk()
    obj.swim()


ob1 = duck()
ob2 = person()

test_game(ob1)
test_game(ob2)
"""
鸭子类型：一个对象的有效语义不是继承自特定的类或者实现特定的方法，而是由当前的属性
         和方法集合决定的，关注的不是对象的类型本身，而是它是如何使用的

在示例中，test_game函数不会管obj是鸭子类型还是人类型，只要实现了walk方法和swim方法就都可以运行
作为对比，在java中如果要写test_game函数，其中obj参数需要明确类型，否则会报错，如果obj指定为duck类型，
那么person类型是无法被采纳的，在Python中一切皆是对象，那么只要传进去就好了
"""


