import os



class Config:
    def __init__(self,cur_path):
        self.cur_path = cur_path
        self.task_name_list = ['不孕症']
        self.task_path_list = [os.path.join(os.path.join(self.cur_path,'data'),task_name) for task_name in self.task_name_list]
        self.model_path = 'model.simple_net'
        self.cross_val_num = 5
        self.epochs_num = 1000
        self.drop_rate = 0.5
        self.random_search_n_iter = 100
        self.random_search_n_jobs = -1
        self.batch_size = 300
        self.model_list = ['SANN','ANN','KNN','SVC','RF']
        self.score_save_path = os.path.join(os.path.join(self.cur_path,'doc'),'score.pkl')
        self.metrics_list = ['accuracy','precision','recall','f1']
        self.random_num = 100
        self.legend_loc = 3
        self.patience_num = 50



if __name__ == '__main__':
    pass