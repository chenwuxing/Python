import copy
"""
赋值：python中解释变量的方法应当是将某个变量分配某个对象，关注的主体
     应当是对象这个物体，变量相当于便利贴，贴在对象这个物体上

可变对象：可变对象是指对象所指向的内存中的值可以改变的
        ->浅拷贝操作会产生新的对象，新瓶装旧酒
        ->深拷贝操作会产生新的对象，新瓶装新酒，完全独立于原来copy的对象,只是值相同，内存中的id已经不相同

不可变对象：不可变对象是指对象所指向的内存中的值不可以被改变，任何试图对其进行改变的操作
            都会产生新的对象
            ->不可变对象的浅拷贝操作和深拷贝操作没区别，都是对原始不可变对象的引用
"""
s0 = [1,'python',[2,3]]
s1 = copy.copy(s0)
s2 = copy.deepcopy(s0)
for i in range(3):
    s_list = [s0,s1,s2]
    print([id(i) for i in s_list[i]])
