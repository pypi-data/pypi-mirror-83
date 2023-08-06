import sys
import os

sys.path.append(os.path.dirname(__file__))

# 导入sann模块的所有包
import configparser




# 定义SANN类
class Sann():
    def __init__(self,input_path,task_name_list):

        cg = configparser.ConfigParser()
        cg['path'] = {'input_path' : input_path,

                             }

        task_name_list_str = ''
        for task_name in task_name_list:
            task_name_list_str += ','
            task_name_list_str += task_name

        cg['task'] = {'task_name_list': task_name_list_str,
                      'cur_task_path': 'None'
                      }

        with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sann'),'initial.ini'), 'w',encoding='utf-8') as f:
            cg.write(f)

        from jhsp.sann.bin import config
        from jhsp.sann.bin import other_utils
        from jhsp.sann.bin import data_utils
        from jhsp.sann.bin import model_utils

        self.config = config.config
        self.other_utils = other_utils.utils
        self.data_utils = data_utils.utils
        self.model_utils = model_utils.utils

# 实例化sann
# 在调用时实例化，因为要传入一个工作目录

sann = Sann('../1/',['不孕症'])
# sann.data_utils.get_weigh_corr(task_path=sann.config.task_path_list[0],force_refresh=True)
# sann.model_utils.get_all_model_best(task_path=sann.config.task_path_list[0],force_refresh=True)
sann.other_utils.get_models2ills_scores(sann.config.task_path_list[0],sann.config.cross_val_num,re_get_score=False,force_refresh=False)
sann.other_utils.plot_epochs_scores(500,task_path=sann.config.task_path_list[0],force_refresh=False)
sann.other_utils.plot_model2ill_score('f1','不孕症',force_refresh=True)












