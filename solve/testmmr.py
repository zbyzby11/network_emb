import codecs
import json
import random

from src.predicate import predicate_new, predicate_ex

DATA_INPUT_DIR = json.load(codecs.open('../config/config.json'))["data_input_dir"]
RESULT_SAVE_DIR = json.load(codecs.open('../config/config.json'))["save_dir"]


def feature_mmr(app_test_dict):
    """
    对测试集进行mmr的计算，基于特征工程的mmr计算
    :param app_test_dict: 输入的测试集，包含app名称和对应的实体的集合
    :return: 每个app的mmr
    """
    test_review = json.load(open('../benchmark/similar.json', 'r', encoding='utf8'))

    train_data = json.load(open('../train/trainapp.json', 'r', encoding='utf8'))

    for i in app_test_dict:
        mmr = 0
        # top20 = list()
        review = test_review[i]  # 保存的基准的相似的列表
        result_list = list()
        entity_set = set(app_test_dict[i])
        # 遍历train_data，求交集的长度
        for app in train_data:
            train_entity_set = set(train_data[app])
            result_list.append((app, len(train_entity_set.intersection(entity_set))))
        result_list.sort(key=lambda x: x[1], reverse=True)
        # result_list = result_list[:30]
        # random.shuffle(result_list)

        for appname, length in result_list:
            if appname == i:
                result_list.remove((appname, length))

        # 计算mmr
        for appname, j in result_list[:20]:
            if appname in review:
                mmr += 1 / (result_list.index((appname, j)) + 1)
        print('{}的MMR为：{}'.format(i, mmr))


def line_mmr(app):
    app2id_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.json', 'r', encoding='utf8'))
    if app2id_dict.get(app, None) == None:
        app_si_dict = predicate_new(app, 20)
        test_review = json.load(open('../benchmark/similar.json', 'r', encoding='utf8'))
        benchmark_app_list = test_review[app]
        predicate_list = app_si_dict[app]
        mmr = 0
        for i in predicate_list:
            if i in benchmark_app_list:
                mmr += 1 / (predicate_list.index(i) + 1)
        print('{}的MMR为：{}'.format(app, mmr))
    else:
        app_si_dict = predicate_ex(app, 20)
        test_review = json.load(open('../benchmark/similar.json', 'r', encoding='utf8'))
        benchmark_app_list = test_review[app]
        predicate_list = app_si_dict[app]
        mmr = 0
        for i in predicate_list:
            if i in benchmark_app_list:
                mmr += 1 / (predicate_list.index(i) + 1)
        print('{}的MMR为：{}'.format(app, mmr))


if __name__ == '__main__':
    app_test_dict = json.load(open('../test/testapp.json', 'r', encoding='utf8'))
    # feature_mmr(app_test_dict)
    for i in app_test_dict:
        line_mmr(i)
    # a = json.load(open('../temp/app3.json','r',encoding='utf8'))
    # l = []
    # for i, j in a.items():
    #     for p ,o in j.items():
    #         if p=='type' and o not in l:
    #             l.append(o)
    # print(l)