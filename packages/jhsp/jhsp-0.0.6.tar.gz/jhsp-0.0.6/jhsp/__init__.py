import importlib



# 导入sann模块的所有包
config = importlib.import_module('sann.bin.config')
other_utils = importlib.import_module('sann.bin.other_utils')
data_utils = importlib.import_module('sann.bin.data_utils')
model_utils = importlib.import_module('sann.bin.model_utils')


# 定义SANN类
class Sann():
    def __init__(self):
        self.config = config.config
        self.other_utils = other_utils.utils
        self.data_utils = data_utils.utils
        self.model_utils = model_utils.utils

# 实例化sann









