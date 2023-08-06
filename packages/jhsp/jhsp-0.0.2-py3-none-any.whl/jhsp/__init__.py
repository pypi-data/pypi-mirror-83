
# 导入sann模块的所有包
from SANN.bin import config
from SANN.bin import other_utils
from SANN.bin import data_utils
from SANN.bin import model_utils




class Sann():
    def __init__(self):
        self.config = config
        self.other_utils = other_utils
        self.data_utils = data_utils
        self.model_utils = model_utils



sann = Sann()


