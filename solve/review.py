import codecs
import json
import random
import re
DATA_INPUT_DIR = json.load(codecs.open('../config/config.json'))["data_input_dir"]
RESULT_SAVE_DIR = json.load(codecs.open('../config/config.json'))["save_dir"]
from src.predicate import predicate_ex, predicate_new


# 找出testset里面50个app的20个相似app，基于特征工程过滤
def basedOnProject():
    testApp = json.load(open('../test/testset.json', 'r', encoding='utf8'))
    trainApp = json.load(open('../train/trainset.json', 'r', encoding='utf8'))

    similar_dict = dict()

    for test_app in testApp:
        # 遍历每个测试app
        entity_set = set(testApp[test_app])
        # 遍历整个训练集，找出与之实体重合最多的app
        result_list = list()
        for train_app in trainApp:
            train_entity_set = set(trainApp[train_app])
            interset = entity_set.intersection(train_entity_set)
            result_list.append((train_app, len(interset)))
            # print(result_list)
        random.shuffle(result_list)
        result_list.sort(key=lambda x: x[1], reverse=True)
        # print(result_list[:50])
        count = 0
        l = list()
        for i, j in result_list:
            if i != test_app:
                l.append(i)
                count += 1
            if count == 100:
                similar_dict[test_app] = l
                break

    f = open('../temp/method1.json','w',encoding='utf8')
    f.write(json.dumps(similar_dict,ensure_ascii=False,indent=4))


def trans2TrainData():
    """
    将训练集转化为和testset相同格式的json文件
    :return:
    """
    train_set = dict()  # 存放训练集的字典

    appid_dict = json.load(open('../data/app2id_dict.txt', 'r', encoding='utf8'))
    app_entity_list = json.load(open('../data/appid2entityids.txt', 'r', encoding='utf8'))
    entity_dict = json.load(open('../data/entity2id_dict.txt', 'r', encoding='utf8'))

    count = 0
    for appname in appid_dict:
        count += 1
        if count % 100 == 0:
            print(count)
        l = list()
        appid = str(appid_dict[appname])
        entity_list = app_entity_list[appid]
        for entityid in entity_list:
            for entity_name, id in entity_dict.items():
                if entityid == id:
                    l.append(entity_name)
        train_set[appname] = l

    f = open('../data/trainset.json', 'w', encoding='utf8')
    f.write(json.dumps(train_set, ensure_ascii=False,indent=4))


def line_method():
    """
    line模型 找出的50个相似的app
    :return: {appname：list[50],...}
    """
    app2id_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    app_test = json.load(open('../test/testset.json', 'r', encoding='utf8'))
    line_dict = dict()
    for i in app_test:
        # appname = app_test[i]
        # print(appname)
        if i in app2id_dict:
            print(1)
            x = predicate_ex(i, 100)
            for i, j in x.items():
                line_dict[i] = j
        else:
            print(1)
            x = predicate_new(i, 100)
            for i, j in x.items():
                line_dict[i] = j
    print(len(line_dict))
    f = open('../temp/method_line.json', 'w', encoding='utf8')
    f.write(json.dumps(line_dict, ensure_ascii=False,indent=4))


def merge_benchmark(file1, file2):
    """
    将两个文件，一个是基于特征工程的文件，一个是基于line模型的文件合并成一个benchmark
    取交集，但是如果不够的话就用line模型的来凑
    :param file1: 文件1
    :param file2: 文件2
    :return:file
    """
    result_dict = dict()
    method1 = json.load(open(file1, 'r', encoding='utf8'))
    method_line = json.load(open(file2, 'r', encoding='utf8'))
    # 遍历line模型的文件
    for line in method_line:
        # 最终的这个app的20个相似app保存的列表
        benchmark_list = []
        t = []
        line_similar_list = method_line[line]
        method1_similar_list = method1[line]
        # 取出一个交集，个数需要达到20个app，如果不够，就在line里面添加
        for i in line_similar_list:
            # 如果有交集，就添加
            if i in method1_similar_list and len(re.sub('[\u4e00-\u9fa5_a-zA-Z0-9]','',i).replace(" ",'')) < 1:
                benchmark_list.append(i)
            else:
                # 如果没有交集，就把它添加到临时列表中
                if len(re.sub('[\u4e00-\u9fa5_a-zA-Z0-9]','',i).replace(" ",''))<1:
                    t.append(i)
        if len(benchmark_list) >= 20:
            # 如果交集大于等于20
            benchmark_list = benchmark_list[:20]
            result_dict[line] = benchmark_list
        else:
            # 如果交集不够20个,就从t中按顺序补上
            benchmark_list.extend(t[:20 - len(benchmark_list)])
            result_dict[line] = benchmark_list
    f = open('../benchmark/similarset.json', 'w', encoding='utf8')
    f.write(json.dumps(result_dict, ensure_ascii=False,indent=4))


if __name__ == '__main__':
    # trans2TrainData()
    # basedOnProject()
    # line_method()
    # merge_benchmark('../temp/method1.json', '../temp/method_line.json')
    a = json.load(open('../benchmark/similarset.json','r',encoding='utf8'))
    for i in a:
        print(len(a[i]))