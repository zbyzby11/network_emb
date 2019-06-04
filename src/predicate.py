import codecs
import json

DATA_INPUT_DIR = json.load(codecs.open('../config/config.json'))["data_input_dir"]

def predicate_exisit(appname):
    app2id_dict = json.load(open(DATA_INPUT_DIR + 'app2id_dict.txt', 'r', encoding='utf8'))
    entity2id_dict = json.load(open(DATA_INPUT_DIR + 'entity2id_dict.txt', 'r', encoding='utf8'))
