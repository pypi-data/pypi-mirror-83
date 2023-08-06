import importlib

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
from os import path, stat
import tensorflow as tf
from sklearn.model_selection import cross_val_score
import pickle
import sklearn
import numpy as np
from os import path
config = importlib.import_module('SANN.bin.config')
data_utils = importlib.import_module('SANN.bin.data_utils')
model_utils = importlib.import_module('SANN.bin.model_utils')


class Utils():
    def __init__(self):
        pass

    def comparison_model(self,model_name_list ):
        with open(config.config.score_save_path, 'rb') as f:
            scores = pickle.load(f)

        for model_name in model_name_list:
            print(model_name)
            for ill_name in config.config.task_name_list:
                print(ill_name)
                for metric_name in config.config.metrics_list:
                    print('{:.2f}'.format(sum(scores[model_name][ill_name][metric_name])/len(scores[model_name][ill_name][metric_name])))

    def get_arguments(self,model_name):

        with open('./data/{}/{}_ini.pkl'.format(config.config.task_name_list[0], model_name), 'rb') as f:
            arguments = pickle.load(f)
            print(','.join(list(arguments.keys())))

        for ill_name in config.config.task_name_list:
            print(ill_name)
            with open('./data/{}/{}_ini.pkl'.format(ill_name,model_name),'rb') as f:
                arguments = pickle.load(f)

                for argument in list(arguments.values()):
                    print(argument,end=',')

                print()

    def plot_epochs_scores(self,epochs_num,task_path,force_refresh=False):

        save_test_loss_path = './doc/' + path.basename(task_path)+'-'+'test_loss'+'.jpg'
        save_test_accuracy_path = './doc/' + path.basename(task_path) + '-' + 'test_accuracy' + '.jpg'

        if path.exists(save_test_loss_path) and path.exists(save_test_accuracy_path):
            print('epochs相关图像已存在，跳过......')
            return None

        plt_y_loss = {'SANN':np.array([0 for i in range(epochs_num)],dtype='float64'),'ANN':np.array([0 for i in range(epochs_num)],dtype='float64')}
        plt_y_accuracy = {'SANN':np.array([0 for i in range(epochs_num)],dtype='float64'),'ANN':np.array([0 for i in range(epochs_num)],dtype='float64')}

        for cur_data in data_utils.utils.get_xy_cross_val(task_path,config.config.cross_val_num):
            train_x, train_y, test_x, test_y, cur_weigh =cur_data


            for model_name in ['SANN','ANN']:


                model = model_utils.utils.get_model(model_name,task_path,initial_weigh=cur_weigh)
                model.compile(loss='categorical_crossentropy', optimizer='adam',
                              metrics=[tf.keras.metrics.CategoricalAccuracy()
                                       ])

                history = model.fit(
                    x=train_x,
                    y=train_y,
                    validation_split=0.2,
                    batch_size=config.config.batch_size,
                    epochs=epochs_num)

                plt_y_loss[model_name] += np.array(history.history['val_loss'])
                plt_y_accuracy[model_name] += np.array(history.history['val_categorical_accuracy'])



        plot_x = [i for i in range(1, epochs_num + 1)]
        plt.plot(plot_x, plt_y_loss['SANN']/config.config.cross_val_num, label='SANN')
        plt.plot(plot_x, plt_y_loss['ANN']/config.config.cross_val_num, label='ANN')
        plt.legend(loc=config.config.legend_loc)
        plt.title(path.basename(task_path)+'-'+'test_loss')

        if force_refresh:
            plt.savefig(save_test_loss_path)

        plt.show()


        plot_x = [i for i in range(1, epochs_num + 1)]
        plt.plot(plot_x, plt_y_accuracy['SANN']/config.config.cross_val_num, label='SANN')
        plt.plot(plot_x, plt_y_accuracy['ANN']/config.config.cross_val_num, label='ANN')
        plt.ylim(0,1)
        plt.legend(loc=config.config.legend_loc)
        plt.title(path.basename(task_path)+'-'+'test_accuracy')

        if force_refresh:
            plt.savefig(save_test_accuracy_path)

        plt.show()

    def plot_models2ills_scores(self,metrics,force_refresh=False):
        with open(config.config.score_save_path, 'rb') as f:
            score = pickle.load(f)

        plt_x = [i for i in range(1,config.config.cross_val_num+1)]

        for task_name in config.config.task_name_list:

            for model_name in config.config.model_list:

                plt.plot(plt_x, score[model_name][task_name][metrics],
                         label=model_name+':'+str(round(sum(score[model_name][task_name][metrics])/len(score[model_name][task_name][metrics]),2)))

            plt.ylim(0.6, 1)
            plt.title(task_name+':Macro_{}'.format(metrics) )
            plt.legend(loc=config.config.legend_loc)

            if force_refresh:
                plt.savefig('./doc/' + task_name + '_Macro_{}.png'.format(metrics))
            plt.show()

    def plot_models2ill_score(self,metrics,task_name,force_refresh=False):
        with open(config.config.score_save_path, 'rb') as f:
            score = pickle.load(f)

        plt_x = [i for i in range(1,config.config.cross_val_num+1)]


        for model_name in config.config.model_list:

            plt.plot(plt_x, score[model_name][task_name][metrics],
                         label=model_name+':'+str(round(sum(score[model_name][task_name][metrics])/len(score[model_name][task_name][metrics]),2)))


        plt.ylim(0.6, 1)
        plt.title(task_name+':Macro_{}'.format(metrics) )
        plt.legend()

        if force_refresh:
            plt.savefig('./doc/' + task_name + '_Macro_{}.png'.format(metrics))
        plt.show()

    def __get_model2ill_scores(self,model_name,task_path,k_num,force_refresh):

        score_dict = {}
        acc_score_list = []
        pre_score_list = []
        rec_score_list = []
        f1_score_list = []


        for i, cur_data in enumerate(data_utils.utils.get_xy_cross_val(task_path=task_path,k=k_num)):


            train_x, train_y, test_x, test_y, cur_weigh = cur_data


            if model_name in ['ANN', 'SANN']:

                temp_save_path = path.join(path.join(path.join(task_path, model_name) , '{}'.format(i)),'')


                model = model_utils.utils.get_model(model_name,task_path,initial_weigh=cur_weigh)

                model.compile(loss='categorical_crossentropy', optimizer='adam',
                              metrics=[tf.keras.metrics.CategoricalAccuracy()
                                       ])

                if path.exists(temp_save_path) and not force_refresh:
                    callbacks = []
                    config.config.epochs_num = 1

                else:
                    callbacks = [
                    tf.keras.callbacks.ModelCheckpoint(filepath=temp_save_path, save_best_only=True,save_weights_only=True,monitor='val_categorical_accuracy',mode='max'),
                    tf.keras.callbacks.EarlyStopping(patience=config.config.patience_num, min_delta=1e-3)
                    ]

                model.fit(
                    x=train_x,
                    y=train_y,
                    validation_data=(test_x, test_y),
                    batch_size=config.config.batch_size,
                    epochs=config.config.epochs_num,
                    callbacks=callbacks)


                model.load_weights(temp_save_path)


                pre_y = model.predict(test_x)
                pre_y = data_utils.utils.onhot2id(pre_y)
                test_y = data_utils.utils.onhot2id(test_y)

            else:

                temp_save_path = path.join(task_path, model_name + '{}_for_score.pkl'.format(i))

                train_y = data_utils.utils.onhot2id(train_y)

                test_y = data_utils.utils.onhot2id(test_y)

                model = model_utils.utils.get_model(model_name, task_path)

                if path.exists(temp_save_path) and not force_refresh:
                    with open(temp_save_path, 'rb') as f:
                        model = pickle.load(f)
                else:
                    model.fit(train_x, train_y)
                    with open(temp_save_path,'wb') as f:
                        pickle.dump(model,f)

                pre_y = model.predict(test_x)


            acc_score_list.append(sklearn.metrics.accuracy_score(test_y,pre_y))

            pre_score_list.append(sklearn.metrics.precision_score(test_y,pre_y, average='macro'))

            rec_score_list.append(sklearn.metrics.recall_score(test_y,pre_y, average='macro'))

            f1_score_list.append(sklearn.metrics.f1_score(test_y,pre_y, average='macro'))



        score_dict['accuracy'] = acc_score_list
        score_dict['precision'] = pre_score_list
        score_dict['recall'] = rec_score_list
        score_dict['f1'] = f1_score_list

        return score_dict

    def reset_model2ill_scores(self,model_name,task_name,k_num):

        force_refresh = True

        task_path = path.join('./data',task_name)

        score_dict = {}
        acc_score_list = []
        pre_score_list = []
        rec_score_list = []
        f1_score_list = []

        for i, cur_data in enumerate(data_utils.utils.get_xy_cross_val(task_path=task_path, k=k_num)):


            train_x, train_y, test_x, test_y, cur_weigh = cur_data

            if model_name in ['ANN', 'SANN']:

                temp_save_path = path.join(path.join(path.join(task_path, model_name) , '{}'.format(i)),'')

                model = model_utils.utils.get_model(model_name, task_path, initial_weigh=cur_weigh)

                model.compile(loss='categorical_crossentropy', optimizer='adam',
                              metrics=[tf.keras.metrics.CategoricalAccuracy()
                                       ])

                if path.exists(temp_save_path) and not force_refresh:
                    callbacks = [

                    ]
                else:
                    callbacks = [
                        tf.keras.callbacks.ModelCheckpoint(filepath=temp_save_path, save_best_only=True,
                                                           save_weights_only=True,monitor='val_categorical_accuracy',mode='max'),
                        tf.keras.callbacks.EarlyStopping(patience=config.config.patience_num, min_delta=1e-3)
                    ]

                model.fit(
                    x=train_x,
                    y=train_y,
                    validation_data=(test_x, test_y),
                    batch_size=config.config.batch_size,
                    epochs=config.config.epochs_num,
                    callbacks=callbacks)

                model.load_weights(temp_save_path)

                pre_y = model.predict(test_x)
                pre_y = data_utils.utils.onhot2id(pre_y)
                test_y = data_utils.utils.onhot2id(test_y)

            else:

                temp_save_path = path.join(task_path, model_name + '{}_for_score.pkl'.format(i))

                train_y = data_utils.utils.onhot2id(train_y)

                test_y = data_utils.utils.onhot2id(test_y)

                model = model_utils.utils.get_model(model_name, task_path)

                if path.exists(temp_save_path) and not force_refresh:
                    with open(temp_save_path, 'rb') as f:
                        model = pickle.load(f)
                else:
                    model.fit(train_x, train_y)
                    with open(temp_save_path, 'wb') as f:
                        pickle.dump(model, f)

                pre_y = model.predict(test_x)

            acc_score_list.append(sklearn.metrics.accuracy_score(test_y, pre_y))

            pre_score_list.append(sklearn.metrics.precision_score(test_y, pre_y, average='macro'))

            rec_score_list.append(sklearn.metrics.recall_score(test_y, pre_y, average='macro'))

            f1_score_list.append(sklearn.metrics.f1_score(test_y, pre_y, average='macro'))

        score_dict['accuracy'] = acc_score_list
        score_dict['precision'] = pre_score_list
        score_dict['recall'] = rec_score_list
        score_dict['f1'] = f1_score_list

        with open(config.config.score_save_path, 'rb') as f:
            score = pickle.load(f)

            score[model_name][path.basename(task_path)] = score_dict

        with open(config.config.score_save_path, 'wb') as f:
            pickle.dump(score, f)

        return score_dict

    def __get_model2ills_scores(self,model_name,k_num,force_refresh):

        model_ills_score = {}

        for task_path in config.config.task_path_list:

            k_score_list = self.__get_model2ill_scores(model_name,task_path,k_num,force_refresh)
            model_ills_score[path.basename(task_path)] = k_score_list

        return model_ills_score

    def get_models2ills_scores(self,k_num,re_get_score=False,force_refresh=False):

        save_path = config.config.score_save_path

        if path.exists(save_path) and not re_get_score:
            if stat(save_path).st_size > 0:
                print('score已存在，跳过......')

                with open(save_path, 'rb') as f:
                    models_ills_scores_dict = pickle.load(f)

                return models_ills_scores_dict

        models_ills_scores_dict = {}      # {model_name:{task_name:{metrics:[k_score]}}}

        for model_name in config.config.model_list:
            model_ills_scores = self.__get_model2ills_scores(model_name,k_num,force_refresh)

            models_ills_scores_dict[model_name] = model_ills_scores

        with open(save_path,'wb') as f:
            pickle.dump(models_ills_scores_dict,f)

        return models_ills_scores_dict










utils = Utils()

if __name__ == '__main__':
    pass

