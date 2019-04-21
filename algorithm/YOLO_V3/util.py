from __future__ import division

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import cv2

def unique(tensor):
    # 因为同一类别可能会有多个真实检测结果
    # 使用unique函数来去除重复
    tensor_np = tensor.cpu().numpy()
    unique_np = np.unique(tensor_np)
    unique_tensor = torch.from_numpy(unique_np)

    # 复制数据
    tensor_res = tensor.new(unique_tensor)
    tensor_res.copy_(unique_tensor)
    return tensor_res


def bbox_iou(box1,box2):
    """
    returns the iou of two bounding boxes
    """
    # get the coordinates of bounding boxes
    b1_x1,b1_y1,b1_x2,b1_y2 = box1[:,0],box1[:,1],box1[:,2],box1[:,3]
    b2_x1,b2_y1,b2_x2,b2_y2 = box2[:,0],box2[:,1],box2[:,2],box2[:,3]

    # get the corrdinates of the intersection rectangle
    inter_rec_x1 = torch.max(b1_x1,b2_x1)
    inter_rec_y1 = torch.max(b1_y1,b2_y1)
    inter_rec_x2 = torch.min(b1_x2,b2_x2)
    inter_rec_y2 = torch.min(b1_y2,b2_y2)

    # intersection area
    inter_area = torch.clamp(inter_rec_x2 - inter_rec_x1 + 1,min=0)*torch.clamp(inter_rec_y2 - inter_rec_y1 + 1,min=0)


    # union area
    b1_area = (b1_x2 - b1_x1 + 1)*(b1_y2 - b1_y1 + 1)
    b2_area = (b2_x2 - b2_x1 + 1)*(b2_y2 - b2_y1 + 1)

    iou = inter_area / (b1_area + b2_area - inter_area)

    return iou

def predict_transform(prediction,inp_dim,anchors,num_classes,CUDA = True):
    """
    在特征图上进行多尺度预测，在grid每个位置都有三个不同尺度的锚点
    predict_transform()利用一个scale得到的feature map预测每个anchor属性(x,y,w,h,s,s_class1,s_class2)
    """
    batch_size = prediction.size(0)
    # stride表示的是整个网络的步长，等于图像原始尺寸与yolo层输入的feature map尺寸相除
    stride = inp_dim // prediction.size(2)
    # feature map每条边格子的数量
    grid_size = inp_dim // stride
    # 一个方框属性个数
    bbox_attrs = 5 + num_classes
    # anchor数量
    num_anchors = len(anchors)
    """
    输入的prediction维度为(batch_size,num_anchors*bbox_attrs,grid_size,grid_size)
    存储方式，将它的维度变换成(batch_size,num_anchors*bbox_attrs,grid_size*grid_size)
    """
    prediction = prediction.view(batch_size,bbox_attrs*num_anchors,grid_size*grid_size)
    # contiguous:view只能用在contiguous的variable上，如果在view之前用了transpose,permute等，需要用contiguous()来
    prediction = prediction.transpose(1,2).contiguous()
    # 将prediction维度转换成(batch_size,grid_size*grid_size*num_anchors,bbox_attrs),不看batch_size
    # (grid_size*grid_size*num_anchors,bbox_attrs)相当于将所有anchor按行排列，即一行对应一个anchor属性，
    prediction = prediction.view(batch_size,grid_size*grid_size*num_anchors,bbox_attrs)
    # 锚点的维度与net块的height和width属性一致，这些属性描述了输入图像的维度，比feature map的规模大


    # sigmoid the tx,ty.and object confidence,tx,ty为预测的坐标偏移值
    prediction[:,:,0] = torch.sigmoid(prediction[:,:,0])
    prediction[:,:,1] = torhc.sigmoid(prediction[:,:,1])
    prediction[:,:,4] = torhc.sigmoid(prediction[:,:,4])

    # 这里生成每个格子的左上角坐标，生成的坐标为grid×grid的二维数组,a,b分别对应这个二维矩阵的x,y坐标的数组
    grid = np.arange(grid_size)
    a,b = np.meshgrid(grid,grid)

    # x_offset即cx,y_offset即cy,表示当前cell左上角坐标
    x_offset = torch.FloatTensor(a).view(-1,1) # view是reshape功能，-1表示自适应
    y_offset = torhc.FloatTensor(b).view(-1,1)

    if CUDA:
        x_offset = x_offset.cuda()
        y_offset = y_offset.cuda()
    
    # 这里的x_y_offset对应的是最终的feature map中每个格子的左上角坐标
    x_y_offset = torch.cat((x_offset,y_offset),1).repeat(1,num_anchors).view(-1,2).unsqueeze(0)

    # bx = sigmoid(tx) + cx,by = sigmoid(ty) + cy
    prediction[:,:,:2] += x_y_offset


    anchors = torch.FloatTensor(anchors)

    if CUDA:
        anchors = anchors.cuda()
    # 这里的anchors本来就是一个长度为6的list(三个anchors每个2个坐标)，然后在0维上进行了grid_size*grid_size个复制
    anchors = anchors.repeat(grid_size*grid_size,1).unsqueeze(0)
    # 对网络预测得到的矩形框的宽高的偏差值进行指数计算，然后乘以anchors里面对应的宽高(grid_size)
    # 论文里公式bw = pw*e^tw,bh = ph*e^th
    prediction[:,:,2:4] = torch.exp(prediction[:,:,2:4])*anchors
    # 这里得到每个anchor中每个类别的得分，将网络预测的每个得分用sigmoid函数计算得到
    prediction[:,:,5:5 + num_classes] = torch.sigmoid((prediction[:,:,5 : 5 + num_classes]))
    
    # 将相对于最终feature map的方框坐标和尺寸映射回输入网络的图片上
    # 将方框的坐标乘以stride即可
    prediction[:,:,:4] *= stride
    return prediction

"""
必须使我们的输出满足objectness分数阈值和非极大值抑制，以得到真实检测结果，要做到这一点，就要使write_results函数的输入为预测结果、
置信度、num_classes和nms_conf(非极大值抑制的阈值)
write_results()首先将网络输出方框属性(x,y,w,h)转换为在网络输入图片416×416坐标系中
方框左上角与右下角坐标(x1,y1)、(x2,y2),然后将方框含有目标得分低于阈值的方框去掉，提取得分最高的那个类的得分max_conf
同时返回这个类对应的序号max_conf_score,然后进行NMS操作。最终每个方框的属性为(ind,x1,y1,x2,y2,s,s_cls,index_cls),ind是这个方框
所属图片在这个batch中的序号，s是这个方框含有目标的得分，s_cls是这个方框中所含目标最有可能的类别的概率得分，index_cls是
s_cls对应的这个类别所对应的序号
"""

def write_results(prediction,confidence,num_classes,nms_conf = 0.4):
    # confidence；输入的预测shape=（1,10647,85)
    # conf_mask:shape=(1,10647)=>增加一维度之后(1,10647,1)
    conf_mask = (prediction[:,:,4] > confidence.float().unsqueeze(2))
    prediction = prediction*conf_mask # 小于置信度的条目值全为0，剩下部分不变
    # 根据numpy的广播原理，它会扩展成与prediction维度一样的tensor

    '''
    保留预测结果中置信度大于阈值的bbox
    下面开始为nms准备
    '''

    # prediction的前五个数据分别表示(cx,cy,w,h,score)，这里创建一个新的数组，大小与prediction的大小相同
    box_corner = prediction.new(prediction.shape)
    '''
    我们可以将我们的框的(中心x,中心y,高度，宽度)属性转换成(左上角x,左上角y,右下角x,右下角y)
    这样做用每个框的两个对角坐标能更轻松的计算两个框的IOU
    '''
    box_corner[:,:,0] = (prediction[:,:,0] - prediction[:,:,2]/2)
    box_corner[:,:,1] = (prediction[:,:,1] - prediction[:,:,3]/2)
    box_corner[:,:,2] = (prediction[:,:,0] + prediction[:,:,2]/2)
    box_corner[:,:,3] = (prediction[:,:,1] + prediction[:,:,3]/2)

    batch_size = prediction.size(0) # 第0个维度是batch_size
    # output = prediction.new(1,prediction.size(2)+1)# shape=(1,85+1)
    # 拼接结果到output中最后返回
    write = False

    '''
    对每一张图片得分的预测值进行NMS操作，因为每张图片的目标数量不一样
    所以有效得分的方框的数量不一样，没法将几张图片同时处理
    所以必须在预测的第一个维度上(batch_size)上遍历每张图片，将得分小于一定分数的去掉
    对剩下的框进行NMS
    '''
    for ind in range(batch_size):
        image_pred = prediction[ind]

        # 最大值索引，最大值，按照dim=1方向计算
        # 只关心有最大值的类别分数
        max_conf,max_conf_score = torch.max(image_pred[:,5:5 + num_classes],1)
        # 维度扩展max_conf:shape=(10647->15)=>(10647->15,1)添加一个列的维度，max_conf变成二维tensor
        # 尺寸为10647*1
        max_conf = max_conf.float().unsqueeze(1)
        max_conf_score = max_conf_score.float().unsqueeze(1)
        # 移除了每一行的80个类别分数，只保留bbox4个坐标
        seq = (img_pred[:,:5],max_conf,max_conf_score)
        '''
        将每个方框的(x1,y1,x2,y2,s)与得分最高的这个类的分数s_cls(max_conf)和
        对应类的序号index_cls
        '''
        image_pred = torch.cat(seq,1)


        non_zero_ind = (torch.nonzero(image_pred[:,4]))
        try:
            image_pred_ = image_pred[non_zero_ind.squeeze(),:].view(-1,7)
        except:
            continue
        
        if image_pred_.shape[0] == 0:
            continue
        
        # get the various classes detected in the images
        img_classes = unique(image_pred_[:,-1]) # -1 index holds the class index

        for cls in img_classes:
            # perform NMS


            # get the detections with one particular class
            cls_mask = image_pred_*(image_pred_[:,-1] ==cls).float().unsqueeze(1)
            class_mask_ind = torch.nonzero(cls_mask[:,-2]).squeeze()
            image_pred_class = image_pred_[class_mask_ind].view(-1,7)

            # sort the detections such that the entry with the maximum objectness
            # confidence is at the top
            conf_sort_index = torch.sort(image_pred_class[:,4],descending = True)[1]
            image_pred_class = image_pred_class[conf_sort_index]
            idx = image_pred_class.size(0) # number of detections


            for i in range(idx):
                # get the IOUs of all boxes that come after the one we are looking at
                # in the loop
                try:
                    ious = bbox_iou(image_pred_class[i].unsqueeze(0),image_pred_class[i+1:])
                except ValueError:
                    break
                except IndexError:
                    break
                
                # zero out all the detections that have IOU > threshold
                iou_mask = (ious < nms_conf).float().unsqueeze(1)
                image_pred_class[i+1:] *= iou_mask


                # remove the non-zero entries
                non_zero_ind = torch.nonzero(image_pred_class[:,4]).squeeze()
                image_pred_class = image_pred_class[non_zero_ind].view(-1,7)

            batch_ind = image_pred_class.new(image_pred_class.size(0),1).fill_(ind)
            seq = batch_ind,image_pred_class

            if not write:
                output = torch.cat(seq,1)
                write = True
            else:
                out = torch.cat(seq,1)
                output = torch.cat(output,out)


    try:
        return output
    except:
        return 0


def letterbox_image(img,inp_dim):
    """
    将图片按照纵横比进行缩放，将空白部分用(128,128,128)进行填充，调整图像尺寸
    具体而言，此时某个边正好等于目标长度，另一边小于等于目标长度
    将缩放后的数据拷贝到画布中心，返回完成缩放
    """
    img_w,img_h = img.shape[1],img.shape[0]
    w,h = inp_dim
    # 取min(w/img_w,h/img_h)这个比例来缩放，缩放后的尺寸为new_w,new_h，即保证较长的边缩后等于目标长宽

    new_w = int(img_w * min(w/img_w,h/img_h))
    new_h = int(img_h * min(w/img_w,h/img_h))
    # 将图片按照纵横比不变来缩放
    resized_image = cv2.resize(img,(new_w,new_h),interpolation = cv2.INTER_CUBIC)
    # 创建一个画布，将resized_image数据拷贝到画布中心
    canvas = np.full((inp_dim[1],inp_dim[0],3),128)

    canvas[(h-new_h)//2:(h-new_h)//2 + new_h,(w-new_w)//2:(w-new_w)//2 + new_w,:] = resized_image

    return canvas

def pre_image(img,inp_dim):
    """
    为网络输入准备图片
    返回一个变量
    """
    img = (letterbox_image(img,(inp_dim,inp_dim)))
    img = img[:,:,::-1].transpose((2,0,1)).copy()
    img = torch.from_numpy(img).float().div(255.0).unsqueeze(0)

    return img

def load_classes(namesfile):
    """
    功能：加载类名文件，load_classes会返回一个字典，将每个类别的
        索引映射到器名称的字符串

    参数：namesfile
    返回：元组，包括类名数组和总类的个数
    """

    fp = open(namesfile,"r")
    names = fp.read().split("\n")[:-1]
    return names





