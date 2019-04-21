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
    """
    参数：
        blocks：形式为列表，其中的每个元素为字典形式，存储着yolo.cfg中的各个块信息
    返回：
        net_info:网络的一些配置参数，结构为字典
        module_list:结构为列表，内部元素为nn.Sequentila创建的序列类型，序列类型元素中装载有
                                cfg文件中的各个网络块，如卷积、上采样等
    """
    # block[0]存储了cfg中[net]的信息，它是一个字典，获取网络输入和预处理相关信息
    """
    [net]
    # Testing
    batch=1
    subdivisions=1
    # Training
    # batch=64
    # subdivisions=16
    width= 320
    height = 320
    channels=3
    momentum=0.9
    decay=0.0005
    angle=0
    saturation = 1.5
    exposure = 1.5
    hue=.1
    """
    net_info = blocks[0]   
    # module_list用于存储每个blcok,每个block对应cfg文件中一个块，类似[convolutional]里面就对应一个卷加块 
    # nn.ModuleList()存储子模型，形式为一个列表
    module_list = nn.ModuleList()   
    #初始值对应于输入数据3通道，用来存储我们需要持续追踪被应用卷积层的卷积核数量(上一层的卷积核数量(特征图深度))
    prev_filters = 3   
    #不仅需要追踪前一层的卷积核数量，还需要追踪之前每个层，随着不断迭代，将每个模块的输出卷积核数量添加到output_filters列表上 
    output_filters = [] 

    for index,x in enumerate(blocks[1:]):
        # 这里的x即是字典，键是对应的操作，值是对应的配置
        module  = nn.Sequential()

        """
        [convolutional]
        batch_normalize=1 
        filters=64 
        size=3 
        stride=1 
        pad=1 
        activation=leaky
        """
        # 卷积层
        if (x["type"] == "convolutional"):  
            # 获取激活函数、批归一化、卷积层参数
            activation = x["activation"]
            try:
                batch_normalize = int(x["batch_normalize"])
                bias = False     #卷积后接BN就不需要bias
            except:
                batch_normalize = 0
                bias = True # 卷积层后无BN层就需要bias
            
            filters = int(x["filters"])
            padding = int(x["pad"])
            kernel_size = int(x["size"])
            stride = int(x["stride"])

            if padding:
                pad = (kernel_size - 1) // 2
            else:
                pad = 0
            # 开始创建并添加相应层
            # nn.Conv2d(self,in_channels,out_channels,kernel_size,stride=1,padding=0,bias=True)
            conv = nn.Conv2d(prev_filters,filters,kernel_size,stride,pad,bias=bias)
            # add_module(name,module)
            module.add_module("conv_{0}".format(index),conv)


            # 添加BN层
            if batch_normalize:
                bn = nn.BatchNorm2d(filters)
                module.add_module("batch_norm{0}".format(index),bn)

            # 检查activation
            # it is either linear or a leaky relu for yolo
            # 给定参数负轴系数0.1
            if activation == "leaky":
                activn = nn.LeakyReLU(0.1，inplace = True)
                module.add_module("leaky_{0}".format(index),activn)
        

        elif(x[""type"] == "upsample"):
            """
            2.upsampling layer
            没有使用Bilinear2dUpsampling
            实际使用的为最近邻插值
            [upsample]
            stride=2
            """
            stride = int(x["stride"])   # 在cfg中就是2，卷积步长为2
            upsample = nn.Upsample(scale_factor = 2,mode = "nearest")
            module.add_module("upsample_{}".format(index),upsample)
        

        # route layer -> Empty layer
        """
        route层的作用，当layer取值为正时，输出这个正数对应的层的特征，如果layer
        取值为负数，输出route层向后退layer层对应的特征
        当属性只有一个值时，它会输出由该值索引的网络层的特征图，示例是-4，所以
        该层级将输出路由层之前第四个层对应的特征图
        当图层有两个值时，它会返回由其值所索引的图层的连接特征图，示例中是-1,61
        该图层将输出来自上一层和第61层拼接的特征图
        """
        elif (x["type"] == "route"):
            """
            [route]
            layers = -4

            [route]
            layers = -1, 61
            """
            x["layers"] = x["layers"].split(',')
            # start of a route
            start = int(x["layers"][0])
            #end,if there exists one
            try:
                end = int(x["layers"][1])
            except:
                end = 0

            # positive anotation:正值
            if start > 0:
                start = start - index

            # 若end>0,由于end = end - index，再执行index + end输出的还是第end层的特征
            if end > 0:
                end = end - index
            
            route = EmptLayer()
            module.add_module("route_{0}".format(index),route)
            if end < 0:# 若end<0,则end还是end,输出index+end(而end<0)故index向后退end层的特征
                # 这里指通道数相加，举例来说26*26*30与26*26*40相互拼接得到的通道数应当是30+40=70
                filters = output_filters[index + start] + output_filters[index + end]
            
            # 如果没有第二个参数，end=0,则对应下面的公式，此时若start>0,由于start = start-index，
            # 再执行index + start得到的还是第start层的特征
            # 若start<0,start还是start，而start<0,则start + index得到的就是index之前第index层的特征图
            else:
                filters = output_filters[index + start]
        

        # shortcut corresponds to skip connection
        elif x["type"] == "shortcut":
            """
            [shortcut]
            from=-3 
            activation=linear 
            """
            shortcut = EmptLayer() #使用空的层，因为它还要执行一个加操作
            module.add_module("shortcut_{}".format(index),shortcut)
        
        elif x["type"] == "yolo":
            """
            [yolo]
            mask = 0,1,2
            anchors = 10,13, 16,30, 33,23, 30,61, 62,45, 59,119, 116,90, 156,198, 373,326
            classes=80
            num=9
            jitter=.3
            ignore_thresh = .5
            truth_thresh = 1
            random=1
            """
            mask = x["mask"].split(",")
            mask = [int(x) for x in mask]

            anchors = x["anchors".split(",")]
            anchors = [int(a) for a in anchors]
            anchors = [(anchors[i],anchors[i+1]) for i in range(0,len(anchors),2)]
            anchors = [anchors[i] for i in mask]


            detection = DetectionLayer(anchors)# 锚点，检测，位置回归，分类
            module.add_module("Detection_{}".format(index),detection)
        

        module_list.append(module)
        prev_filters = filters
        output_filters.append(filters)
    
    return (net_info,module_list)

class Darknet(nn.Module):
    """
    实现了网络的前向传播函数以及载入预训练的网络权重参数
    """
    def __init__(self,cfgfile):

        super(Darknet,self).__init__()
        # self.blocks结构是列表，其中的每个元素是字典结构，装有块信息
        self.blocks = parse_cfg(cfgfile)
        # 调用create_modules函数，self.net_info是整个网络的一些全局参数配置
        # self.module_list的结构是列表，由nn.ModuleList创建，列表中的元素为nn.Sequential()结构，装载着网络模块的各个操作
        self.net_info,self.module_list = create_modules(self.blocks)

    def forward(self,x,CUDA):
        """
        功能：实现网络的前向传播
        参数：
            x:输入数据
            CUDA:是否使用gpu加速
        返回：检测结果
        """
        # 除了net块之外的所有，forward这里用的是blocks列表中的各个block块字典
        modules = self.blocks[1:]
        # we cache the outputs for the route layer
        outputs = {}

        # write表示是否遇到第一个检测，write=0，则收集器尚未初始化，
        # write=1,收集器已经初始化，只需要将收集器和检测图级联起来即可
        write = 0
        
        # modules是一个列表，元素为字典
        for i,module in enumerate(modules):
            # 得到这个字典对应的块操作类型
            module_type = (module["type"])

            if module_type == "convolutional" or module_type == "upsample":
                x = self.module_list[i](x)

            elif module_type == "route":
                layers = module["layers"]
                layers = [int(a) for a in layers]

                if (layers[0]) > 0：
                    layers[0] = layers[0] - i
                # 如果只有一层时，从前面的if (layers[0]) >0:语句知，如果layer[0]>0,则输出的就是当前layer
                if len(layers) == 1:
                    x = outputs[i + (layers[0])]
                # 第二个元素同理
                else:
                    if (layers[1]) > 0:
                        layers[1] = layers[1] - i
                    
                    map1 = outputs[i + layers[0]]
                    map2 = outputs[i + layers[1]]
                    #第二个参数设为1，这是因为我们希望将特征图沿anchor数量的维度级联起来
                    x = torch.cat((map1,map2),1)
                

            elif module_type == "shortcut":
                from_  = int(module["from"])
                # 求和运算，只是将前一层的特征图添加到后面的层上而已
                x = outputs[i-1] + outputs[i+from_] 
                
            elif module_type == 'yolo':
                anchors = self.module_list[i][0].anchors
                # 从net_info(实际就是block[0],即[net])中get the input dimensions
                inp_dim = int(self.net_info["height"])
                
                # get the number of classes
                num_classes = int(module["classes"])

                # transform
                x = x.data # 这里得到的是预测的yolo层feature map
                # 在util.py中的predict_transform()函数利用x(是传入yolo层的feature map),
                # 得到每个格子所对应的anchor最终得到的目标
                x = predict_transform(x,inp_dim,anchors,num_classes,CUDA)

                if not write:   # if no collector has been initialied
                    # 因为一个空的tensor无法与一个有数据的tensor进行concatenate操作
                    detections = x
                    # 用write=1进行标记，当后面的分数出来后，直接进行concatenate操作即可
                    write = 1
                else:
                    """
                变换后x的维度是(batch_size,grid_size*grid_size*num_anchors,5+类别数量)，这里是在维度1上进行concatenate,
                即按照anchor数量的维度进行连接。yolov3中有3个yolo层，所以对于每个yolo层的输出先用predict_transform()变成
                每行为一个anchor对应的预测值的形式(不看batch_size这个维度，x剩下的维度可以看成一个二维tensor)，这样3个yolo层
                的预测值按照每个方框对应的行的维度进行连接。得到了这张图所有anchor的预测值
                    """
                    detections = torch.cat((detections,x),1)# 将在3个不同level的feature map上检测结果存储在detections
            outputs[i] = x
        return detections

# blocks = parse_cfg('cfg/yolov3.cfg')
# x,y = create_modules(blocks)
# print(y)
    def load_weights(self,weightfile):
        # open the weights file
        fp = open(weightfile,"rb")

        # the first 5 values are header information
        #1.major version number
        #2. minor version number
        #3.subversion number
        #4,5. Images seen by the network(during training)
        header = np.fromfile(fp,dtype = np.int32,count = 5)
        self.header = torch.from_numpy(header)
        self.seen = self.header[3]

        weights = np.fromfile(fp,dtype = np.float32) # 加载np.ndarray中的剩余权重，权重是以float32类型存储

        ptr = 0
        for i in range(len(self.module_list)):
            # blocks中的第一个元素是网络参数和图像的描述，所以跳过它
            module_type = self.blocks[i + 1]["type"]

            # if module_type is convolutional load weights
            # otherwise ignore
            if module_type == "convolutional":
                model = self.module_list[i]
                try:
                    batch_normalize = int(self.blocks[i+1]["batch_normalize"])
                else:
                    batch_normalize = 0
                conv = model[0]

                if (batch_normalize):
                    bn = model[1]

                    # get the number of weights of batch norm layer
                    num_bn_biases = bn.bias.numel()

                    # load the weights
                    bn_biases = torch.from_numpy(weights[ptr:ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_weights = torch.from_numpy(weights[ptr:ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_running_mean = torch.from_numpy(weights[ptr:ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_running_var = torch.from_numpy(weights[ptr:ptr + num_bn_biases])
                    ptr += num_bn_biases

                    #cast the loaded weights into dims of model weights
                    bn_biases = bn_biases.view_as(bn.bias.data)
                    bn_weights = bn_weights.view_as(bn.weight.data)
                    bn_running_mean = bn_running_mean.view_as(bn.bn_running_mean)
                    bn_running_var = bn_running_var.view_as(bn.bn_running_var)

                    # copy the data to model
                    bn.bias.data.copy_(bn_biases)
                    bn.weight.data.copy_(bn_weights)
                    bn.bn_running_mean.copy_(bn_running_mean)
                    bn.bn_running_var.copy_(bn_running_var)
                
                else:#如果batch_normalize 的检测结果不是True,只需要加载卷积层的偏置项
                    # number of biases
                    num_biases = conv.bias.numel()

                    # load the weights
                    conv_biases = torch.from_numpy(weights[ptr:ptr + num_biases])
                    ptr = ptr + num_biases

                    #reshape the loaded weights according to the dims of the model weights
                    conv_biases = conv_biases.view_as(conv.bias.data)

                    # finally copy the data
                    conv.bias.data.copy_(conv_biases)


                # let us load the weights for the convolutional layers
                num_weights = conv.weight.numel()

                # do the same as above for weights
                conv_weights = torch.from_numpy(weights[ptr:ptr+num_weights])
                ptr = ptr + num_weights

                conv_weights = conv_weights.view_as(conv.weight.data)
                conv.weight.data.copy_(conv_weights)

    
            








    









