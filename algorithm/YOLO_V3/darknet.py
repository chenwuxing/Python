from __future__ import division


import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from util import *


def parse_cfg(cfgfile):
    """
    参数：配置文件路径
    返回值：列表对象，其中每一个元素为一个字典类型，对应于一个要建立的神经网络模块层
    """
    # 加载文件并过滤掉文本中多余内容
    file = open(cfgfile,'r')
    lines = file.read().split('\n')
    lines = [x for x in lines if len(x) > 0] # 去掉空行
    lines = [x for x in lines if x[0] != '#'] # 取掉以#开头的注释行
    lines = [x.rstrip().lstrip() for x in lines] # 取掉左右两边的空格

    # cfg文件中的每个块用{}括起来，最后组成一个列表，一个block存储一个块的内容，即每个层用一个字典block存储
    block = {}
    blocks = []

    for line in lines:
        if line[0] == "[":  # cfg文件中一个层块的开始
            if len(block) != 0: # 如果块内已经存储了信息，说明是上一个块的信息还没有被保存
                blocks.append(block) # 那么这个块加入到blocks列表中
                block = {}  # 覆盖已经存储的block,创建一个空白块存储描述下一个块的信息
            block["type"] = line[1:-1].rstrip() # 把cfg的[]中的块名作为键type的值
            else:
                key,value = line.split('=') #按等号分割
                block[key.rstrip()] = value.lstrip() # 左边是key(去掉左空格)，右边是value(去掉左空格)
    blocks.append(block)    #退出循环，将最后一个未加入的block加进去
    return blocks

# 配置文件定义了6种不同type
# 'net':相当于超参数，网络全局配置的相关参数
# {'convolutional','net','route','shortcut','upsample','yolo'}
# cfg = parse_cfg('cfg/yolov3.cfg')
#print(cfg)

class EmptLayer(nn.Module):
    """
    为shortcut layer/route layer准备，具体功能不在此实现，在Darknet类的forward函数中有实现
    """
    def __init__(self):
        super(EmptLayer,self).__init__()


class DetectionLayer(nn.Module):
    """yolo检测层的具体实现，在特征图上使用锚点预测目标区域和类别，功能函数在predict_transform中
    """
    def __init__(self,anchors):
        super(DetectionLayer,self).__init__()
        self.anchors = anchors


def create_modules(blocks):
    net_info = blocks[0]    # block[0]存储了cfg中[net]的信息，它是一个字典，获取网络输入和预处理相关信息
    module_list = nn.ModuleList()   # module_list用于存储每个blcok,每个block对应cfg文件中一个块，类似[convolutional]里面就对应一个卷加块
    prev_filters = 3    #初始值对应于输入数据3通道，用来存储我们需要持续追踪被应用卷积层的卷积核数量(上一层的卷积核数量(特征图深度))
    output_filters = [] # 不仅需要追踪前一层的卷积核数量，还需要追踪之前每个层，随着不断迭代，将每个模块的输出卷积核数量添加到output_filters列表上
    









