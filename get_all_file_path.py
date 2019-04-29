import os

def get_path(root,all_file_path):
    '''
    功能：递归得到给定路径下所有文件的路径
    参数：
        root:指定路径，文件夹or文件
        all_file_path:用来存文件路径
    返回值：
        all_file_path:存放文件路径的列表

    '''
    if os.path.isdir(root):
        for files in os.listdir(root):
            sub_path = os.path.join(root,files).replace('\\','/')
            get_path(sub_path,all_file_path)
    else:
        all_file_path.append(root)
    return all_file_path




