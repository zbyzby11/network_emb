import codecs
import json
import time

import numpy as np
import torch as t

DATA_INPUT_DIR = json.load(codecs.open('../config/config.json'))["data_input_dir"]
RESULT_SAVE_DIR = json.load(codecs.open('../config/config.json'))["save_dir"]


def predicate_ex(appname, k):
    app2id_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    entity2id_dict = json.load(open(DATA_INPUT_DIR + 'entity2id_dict.txt', 'r', encoding='utf8'))

    app_emb = json.load(open(RESULT_SAVE_DIR + 'appEmbedding.txt', 'r', encoding='utf8'))
    entity_emb = json.load(open(RESULT_SAVE_DIR + 'entityEmbedding.txt', 'r', encoding='utf8'))
    all_emb = np.array(app_emb)
    app_index = app2id_dict.get(appname, None)
    l = []
    if app_index is not None:
        app_embedding = np.array(app_emb[app_index])
        result_tensor = np.sqrt(np.sum((app_embedding - all_emb) ** 2, axis=1))
        x = np.argsort(result_tensor)[1:k + 1]
        for predicate_index in x:
            for app, index in app2id_dict.items():
                if index == predicate_index:
                    l.append(app)
    return {appname: l}


# 使用实体的平均的向量来表示这个app的向量来进行预测
def predicate_new(appname, k):
    """
    预测测试集中的app的top-k个相似的app
    :param appname: 预测的app的名字
    :param k: 预测前k个相似
    :return: app对应的相似app的列表组成的字典{appnaem:list}
    """
    app_test_dict = json.load(open('../test/testset.json', 'r', encoding='utf8'))
    # print(app_test_dict[appname])
    appid_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    entityid_dict = json.load(open(DATA_INPUT_DIR + 'entity2id_dict.txt', 'r', encoding='utf8'))
    app_avg_emb = json.load(open(RESULT_SAVE_DIR + 'appEmbeddingAverageEntity.txt', 'r', encoding='utf8'))
    entity_emb = json.load(open(RESULT_SAVE_DIR + 'entityEmbedding.txt', 'r', encoding='utf8'))
    app_emb = json.load(open(RESULT_SAVE_DIR + 'appEmbedding.txt', 'r', encoding='utf8'))

    test_appentity_list = app_test_dict[appname]
    # 测试集中app的向量表示，用他所包含的实体的平均向量表示，初始化为同app_avg_emb的第二个维度
    app_test_vec = np.zeros(np.array(app_avg_emb).shape[1])
    entity_test_id = [entityid_dict[entity_name] for entity_name in test_appentity_list if
                      entity_name in entityid_dict.keys()]
    # 记录有效的实体的个数
    entity_num = 0
    for entity_id in entity_test_id:
        app_test_vec = np.add(app_test_vec, entity_emb[entity_id])
        entity_num += 1
    # 得出平均后的向量
    app_test_vec = app_test_vec / entity_num
    # 进行预测
    # 判断app_list中与app按相似程序降序的app列表
    res = []
    for appid in range(len(app_avg_emb)):
        tmp = np.sum((app_test_vec - np.array(app_avg_emb[appid])) ** 2)
        res.append(tmp)
    res = np.array(res)
    # 带索引的排好序的距离由小到大的排序
    sorted_appids = np.argsort(res)
    if appid_dict.get(appname, ' ') != ' ':
        sorted_appids = np.delete(sorted_appids, sorted_appids[appid_dict.get(appname)])
    sorted_appids = sorted_appids[:k]

    l = []
    for app, appid in appid_dict.items():
        for id in sorted_appids:
            if id == appid:
                l.append(app)
    # print(l)
    return {appname: l}


if __name__ == '__main__':
    # s = time.time()
    # x = predicate_ex('Facebook Lite',10)
    # print(x)
    # print(time.time()-s)
    # x = predicate_new('微博', 20)
    # print(x)
    appid_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    test_data = json.load(open('../test/testset.json', 'r', encoding='utf8'))
    for app in test_data:
        if app in appid_dict:
            a = predicate_ex(app, 20)
            print(a)
        else:
            a = predicate_new(app, 20)
            print(a)
