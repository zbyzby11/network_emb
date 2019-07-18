"""
将这里的app和实体转化为OPENNE的输入格式
"""
import json
import codecs


def trans2line(file):
    """
    将原始的json文件转化成四个line模型的输入
    :param file: 输入的json文件
    :return: 四个文件
    """
    trainapp = json.load(open(file, 'r', encoding='utf8'))
    appid = json.load(open('../data/app2id_dict.json', 'r', encoding='utf8'))
    entityid = json.load(open('../data/entity2id_dict.json', 'r', encoding='utf8'))
    # appid_dict = dict()
    # app_entity_pairs = list()
    # appid2ntityid_dict = dict()
    # entityid_dict = dict()
    # 建立app名称和index的字典
    # for appname, entity_list in trainapp.items():
    #     appid_dict[appname] = len(appid_dict)
    # f = open('../data/app2id_dict.json', 'w', encoding='utf8')
    # f.write(json.dumps(appid_dict, ensure_ascii=False, indent=4))

    # 建立实体名称和index的字典
    # for appname, entity_list in trainapp.items():
    #     for entity in entity_list:
    #         if entity not in entityid_dict:
    #             entityid_dict[entity] = len(entityid_dict)
    # f = open('../data/entity2id_dict.json', 'w', encoding='utf8')
    # f.write(json.dumps(entityid_dict, ensure_ascii=False, indent=4))

    # #建立app和实体之间对应关系
    # app_entity_list = []
    # for appname, entity_list in trainapp.items():
    #     app_id = appid[appname]
    #     for entity in entity_list:
    #         entity_id = entityid[entity]
    #         app_entity_list.append((app_id,entity_id))
    # f = open('../data/app_entity_pairs_id.txt', 'w', encoding='utf8')
    # f.write(json.dumps(app_entity_list, ensure_ascii=False))

    # 建立app和实体之间对应关系字典
    appentity_dict = dict()
    for appname, entity_list in trainapp.items():
        app_id = appid[appname]
        l = []
        for entity in entity_list:
            entity_id = entityid[entity]
            l.append(entity_id)
        appentity_dict[app_id] = l

    f = open('../data/appid2entity.json', 'w', encoding='utf8')
    f.write(json.dumps(appentity_dict, ensure_ascii=False))


def trans2openne(app2idtxt, entity2idtxt, app_entity_pairs):
    """
    将实体的索引字典的index改变index值
    :param app2idtxt: app索引
    :param entity2idtxt: 实体索引
    :param app_entity_pairs: app实体对
    :return: 一个新文件，格式为node1 node2
                              noden，nodek....
    """
    appid = json.load(codecs.open(app2idtxt, 'r', encoding='utf8'))
    entityid = json.load(codecs.open(entity2idtxt, 'r', encoding='utf8'))
    app_entity = json.load(codecs.open(app_entity_pairs, 'r', encoding='utf8'))

    for entity_name in list(entityid.keys()):
        entityid[entity_name] += len(appid)

    f = open('../inputforne/app_index.json', 'w', encoding='utf8')
    f.write(json.dumps(appid, ensure_ascii=False, indent=4))
    f.close()

    f1 = open('../inputforne/entity_index.json', 'w', encoding='utf8')
    f1.write(json.dumps(entityid, ensure_ascii=False, indent=4))
    f1.close()

    with open('../inputforne/edjlist.txt', 'w', encoding='utf8') as f:
        for i, j in app_entity:
            f.write(str(i) + ' ' + str(j + len(appid)) + '\n')


if __name__ == '__main__':
    # trans2openne('../data/app2id_dict.txt','../data/entity2id_dict.txt','../data/app_entity_pairs_id.txt')
    trans2line('../data/trainapp.json')
