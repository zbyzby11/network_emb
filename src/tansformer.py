"""
将这里的app和实体转化为OPENNE的输入格式
"""
import json
import codecs

def trans2openne(app2idtxt,entity2idtxt,app_entity_pairs):
    """
    将实体的索引字典的index改变index值
    :param app2idtxt: app索引
    :param entity2idtxt: 实体索引
    :param app_entity_pairs: app实体对
    :return: 一个新文件，格式为node1 node2
                              noden，nodek....
    """
    appid = json.load(codecs.open(app2idtxt,'r',encoding='utf8'))
    entityid = json.load(codecs.open(entity2idtxt,'r',encoding='utf8'))
    app_entity = json.load(codecs.open(app_entity_pairs,'r',encoding='utf8'))

    for entity_name in list(entityid.keys()):
        entityid[entity_name] += len(appid)

    f = open('../inputforne/app_index.json','w',encoding='utf8')
    f.write(json.dumps(appid,ensure_ascii=False,indent=4))
    f.close()

    f1 = open('../inputforne/entity_index.json','w',encoding='utf8')
    f1.write(json.dumps(entityid,ensure_ascii=False,indent=4))
    f1.close()

    with open('../inputforne/edjlist.txt','w',encoding='utf8') as f:
        for i,j in app_entity:
            f.write(str(i)+' '+str(j+len(appid))+'\n')




if __name__ == '__main__':
    trans2openne('../data/app2id_dict.txt','../data/entity2id_dict.txt','../data/app_entity_pairs_id.txt')