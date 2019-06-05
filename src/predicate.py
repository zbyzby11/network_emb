import codecs
import json
import numpy as np
import torch as t

DATA_INPUT_DIR = json.load(codecs.open('../config/config.json'))["data_input_dir"]
RESULT_SAVE_DIR = json.load(codecs.open('../config/config.json'))["save_dir"]

def predicate_exisit(appname,k):
    app2id_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    entity2id_dict = json.load(open(DATA_INPUT_DIR + 'entity2id_dict.txt', 'r', encoding='utf8'))

    app_emb_dict = json.load(open(RESULT_SAVE_DIR + 'app_emb.json','r',encoding='utf8'))
    entity_emb_dict = json.load(open(RESULT_SAVE_DIR + 'entity_emb.json','r',encoding='utf8'))

    all_app_embedding = list()
    for index,emb in app_emb_dict.items():
        all_app_embedding.append(emb)
    all_embedding = t.Tensor(all_app_embedding)

    app_index = app2id_dict.get(appname,None)
    if app_index is not None:
        app_embedding = t.Tensor(app_emb_dict.get(str(app_index),None))
        temp_tensor = t.mul(app_embedding,all_embedding)
        sum_tensor = t.sum(temp_tensor,dim=1)
        x = t.argsort(sum_tensor)[:k]
        print(x)
        for predicate_index in x:
            for appname,index in app2id_dict.items():
                if index == predicate_index:
                    print(appname)
    else:
        raise IndexError

if __name__ == '__main__':
    predicate_exisit('Gmail',10)
