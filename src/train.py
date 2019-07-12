from net2vec import Net2vec

from data_preprocess import get_existed_train_data

if __name__ == '__main__':
    app_entity_pairs, appid2entityids, app2id_dict, entity2id_dict = get_existed_train_data()
    print('数据预处理完成')

    app_count = len(list(app2id_dict.keys()))
    entity_count = len(list(entity2id_dict.keys()))

    w2v = Net2vec(app_entity_pairs, appid2entityids, app_count, entity_count)
    w2v.train()
