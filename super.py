def super(cls,inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]

"""
super函数功能：
            ->查找inst的mro列表
            ->查找cls在当前mro列表中的index,并返回其下一个位置的类
"""
