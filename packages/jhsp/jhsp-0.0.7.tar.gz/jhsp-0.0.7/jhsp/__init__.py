import importlib
import sys
import os
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__),'sann'),'bin'))
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__),'sann'),'model'))


# 导入sann模块的所有包

config = importlib.import_module('config')
other_utils = importlib.import_module('other_utils')
data_utils = importlib.import_module('data_utils')
model_utils = importlib.import_module('model_utils')


# 定义SANN类
class Sann():
    def __init__(self,cur_path):
        self.config = config.Config(cur_path)
        self.other_utils = other_utils.utils
        self.data_utils = data_utils.utils
        self.model_utils = model_utils.utils

# 实例化sann









