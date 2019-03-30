import os
import cv2


def change_ext(path,old_ext,new_ext,out_path):
    for parent,dir_name,files in os.walk(path):
        # 遍历文件夹下的文件
        for file in files:
            # 文件的绝对路径
            img_path = os.path.join(parent,file).replace('\\','/')
            # 判断文件是否是要求的后缀
            if file.endswith(old_ext):
                # 读入文件
                img = cv2.imread(img_path)
                trans = parent.replace('\\','/')    # windows下路径拼接符号默认为'\',需要进行替换一下
                part_path_list = trans.split('/')
                part_path = '/'.join(part_path_list[1:])
                save_path = out_path + part_path
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                # 将旧的扩展名更换为新的扩展名
                tmp = file.replace(old_ext,new_ext)
                # 新的存放位置
                position = save_path + '/' + tmp
                cv2.imwrite(position,img)
change_ext('g:/test','bmp','jpg','e:/')




