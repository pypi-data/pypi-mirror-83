import sys
import os

sys.path.append(os.path.dirname(__file__))

# 导入sann模块的所有包
import configparser
from jhsp.sann.bin import config
from jhsp.sann.bin import other_utils
from jhsp.sann.bin import data_utils
from jhsp.sann.bin import model_utils



# 定义SANN类
class Sann():
    def __init__(self,input_path,output_path,task_name_list):

        cg = configparser.ConfigParser()
        cg['path'] = {'input_path' : input_path,
                     'output_path' : output_path
                             }

        task_name_list_str = ''
        for task_name in task_name_list:
            task_name_list_str += ','
            task_name_list_str += task_name

        cg['task'] = {'task_name_list': task_name_list_str}


        with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sann'),'initial.ini'), 'w') as f:
            cg.write(f)


        self.config = config.config
        self.other_utils = other_utils.utils
        self.data_utils = data_utils.utils
        self.model_utils = model_utils.utils

# 实例化sann
# 在调用时实例化，因为要传入一个工作目录












