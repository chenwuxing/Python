#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import os
from data.config import cfg
import cv2


# 利用wider face中附带的wider_face_train_bbx_gt.txt产生新的训练标签和测试标签
WIDER_ROOT = os.path.join(cfg.HOME, 'WIDER')
WIDER_ROOT = WIDER_ROOT.replace('\\','/')

train_list_file = os.path.join(WIDER_ROOT, 'wider_face_split',
                               'wider_face_train_bbx_gt.txt')
train_list_file = train_list_file.replace('\\','/')

val_list_file = os.path.join(WIDER_ROOT, 'wider_face_split',
                             'wider_face_val_bbx_gt.txt')
val_list_file = val_list_file.replace('\\','/')


WIDER_TRAIN = os.path.join(WIDER_ROOT, 'WIDER_train', 'images')
WIDER_TRAIN = WIDER_TRAIN.replace('\\','/')

WIDER_VAL = os.path.join(WIDER_ROOT, 'WIDER_val', 'images')
WIDER_VAL = WIDER_VAL.replace('\\','/')



def parse_wider_file(root, file):
    # 读取文件
    with open(file, 'r') as fr:
        lines = fr.readlines()
    # 记录信息
    face_count = []
    img_paths = []
    face_loc = []
    img_faces = []
    count = 0
    flag = False
    for k, line in enumerate(lines):
        line = line.strip().strip('\n')
        if count > 0:
            line = line.split(' ')
            count -= 1
            loc = [int(line[0]), int(line[1]), int(line[2]), int(line[3])]
            face_loc += [loc]
        if flag:
            face_count += [int(line)]
            flag = False
            count = int(line)
        if 'jpg' in line:
            img_paths += [os.path.join(root, line).replace('\\','/')] #这一句在windows下产生的路径需要进行修改
            flag = True

    total_face = 0
    for k in face_count:
        face_ = []
        for x in range(total_face, total_face + k):
            face_.append(face_loc[x])
        img_faces += [face_]
        total_face += k
    return img_paths, img_faces


def wider_data_file():
    # 接收parse_wider_file函数返回的图片路径信息和图片中人脸信息
    img_paths, bbox = parse_wider_file(WIDER_TRAIN, train_list_file)
    fw = open(cfg.FACE.TRAIN_FILE, 'w')
    for index in range(len(img_paths)):
        path = img_paths[index]
        boxes = bbox[index]
        fw.write(path)
        fw.write(' {}'.format(len(boxes)))
        for box in boxes:
            data = ' {} {} {} {} {}'.format(box[0], box[1], box[2], box[3], 1)
            fw.write(data)
        fw.write('\n')
    fw.close()

    img_paths, bbox = parse_wider_file(WIDER_VAL, val_list_file)
    fw = open(cfg.FACE.VAL_FILE, 'w')
    for index in range(len(img_paths)):
        path = img_paths[index]
        boxes = bbox[index]
        fw.write(path)
        fw.write(' {}'.format(len(boxes)))
        for box in boxes:
            data = ' {} {} {} {} {}'.format(box[0], box[1], box[2], box[3], 1)
            fw.write(data)
        fw.write('\n')
    fw.close()


if __name__ == '__main__':
    wider_data_file()
