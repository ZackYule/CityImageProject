import pandas as pd
import jieba.analyse as analyse
import setting
from utils import *

DataFilePath = 'data/西安城市形象数据.pkl'


def get_key_word_from_a_doc(content, topK=10, allow_pos_list=('n','nz','vn')):
    return ' '.join(analyse.extract_tags(content, topK, allowPOS=allow_pos_list))


if __name__ == "__main__":
    data = pd.read_pickle(DataFilePath)
    analyse.set_idf_path(setting.IDFFilePath)
    analyse.set_stop_words(setting.StopWordPath)
    data['关键词'] = data['内容'].apply(get_key_word_from_a_doc, args=(setting.KeywordTopNumber, setting.AllowPOSList))
    data.to_pickle(get_new_path(DataFilePath, '关键词'))
