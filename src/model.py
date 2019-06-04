"""
LINE模型的定义，主要重写nn.Module下的forward方法和实现保存模型参数的方法
"""
import json

import torch as t
import numpy as np

from torch import nn
from torch.functional import F

class LINE(nn.Module):
    def __init__(self,app_count,entity_count,embedding_dim):
        """
        Line模型的初始化
        :param app_count:app的数量
        :param entity_count:实体的数量
        :param embedding_dim:embedding的维度
        """
        super(LINE,self).__init__()
        self.app_count = app_count  # app数量
        self.entity_count = entity_count  # 实体数量
        self.embedding_dim = embedding_dim
        self.app_emb = nn.Embedding(app_count,embedding_dim,sparse=True)
        self.entity_emb = nn.Embedding(entity_count,embedding_dim,sparse=True)
        self.init_weight()

    def init_weight(self):
        """
        模型参数的初始化
        :return: None
        """
        nn.init.xavier_uniform(self.app_emb.weight.data)
        nn.init.xavier_uniform(self.entity_emb.weight.data)

    def forward(self,pos_app,pos_entity,neg_app,neg_entity):
        """
        重写forward函数，传入四个Variable
        :param pos_app: 正例app
        :param pos_entity: 正例实体
        :param neg_app: 负例app
        :param neg_entity: 负例实体
        :return: 损失函数的值
        """
        #正例得分
        pos_emb_app = self.app_emb(pos_app)
        pos_emb_entity = self.entity_emb(pos_entity)
        pos_score = t.mul(pos_emb_app, pos_emb_entity)
        pos_score = t.sum(pos_score, dim=1)
        pos_score = F.logsigmoid(pos_score)
        #负例得分
        neg_emb_app = self.app_emb(neg_app)
        neg_emb_entity = self.entity_emb(neg_entity)
        neg_score = t.mul(neg_emb_app, neg_emb_entity)
        neg_score = t.sum(neg_score, dim=1)
        neg_score = F.logsigmoid(-1 * neg_score)
        #总得分
        pos_score_sum = t.sum(pos_score)
        neg_score_sum = t.sum(neg_score)
        all_score = -1 * (pos_score_sum + neg_score_sum)

        return all_score


    def save_para(self,file_dir):
        """
        保存模型的参数，主要是caseid的embedding矩阵和entityid的embedding矩阵
        :param filename: 保存的文件路径
        :return: 两个文件，每个文件为字典格式，一个是保存案件id embedding的文件字典，
                一个是保存entityid embedding的文件字典
        """
        app_emb = self.app_emb.weight.data.detach().cpu().numpy().tolist()
        entity_emb = self.entity_emb.weight.data.detach().cpu().tolist()

        #appid的embedding矩阵
        app_f = open(file_dir + 'app_emb.txt','w',encoding='utf8')
        app_f.write(json.dumps(app_emb,ensure_ascii=False))
        app_f.close()

        #实体id的embedding矩阵
        entity_f = open(file_dir + 'entity_emb.txt','w',encoding='utf8')
        entity_f.write(json.dumps(entity_emb,ensure_ascii=False))
        entity_f.close()

        #todo:对于新的案件，需要先找出与其关联的实体的embedding，并求平均，
        # 用平均值来表示这个案件的embedding，所以需要对每个训练的案件都进行这个操作
        # 需要保存一个文件，保存每个案件的平均embedding向量

