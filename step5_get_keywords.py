import pandas as pd
import jieba.analyse as analyse
import setting
from utils import *

DataFilePath = 'data/西安城市形象数据.pkl'
DictionaryFilePath = 'data/西安城市形象编码词表.pkl'

def get_key_word_from_a_doc(content, topK=10, allow_pos_list=('n','nz','vn')):
    return ' '.join(analyse.extract_tags(content, topK, allowPOS=allow_pos_list))


if __name__ == "__main__":
    # 读取数据
    data = pd.read_pickle(DataFilePath)
    dictionary_comparison_table = pd.read_pickle(DictionaryFilePath)
    dictionary_comparison_table_topic = dictionary_comparison_table.drop(['积极判断框架','消极判断框架','事件框架','细节框架'], axis=1)
    dictionary_comparison_table_narration = dictionary_comparison_table[['积极判断框架','消极判断框架','事件框架','细节框架']]
    # 设置
    analyse.set_idf_path(setting.IDFFilePath)
    analyse.set_stop_words(setting.StopWordPath)
    # 选取关键词
    data['关键词'] = data['内容'].apply(get_key_word_from_a_doc, args=(setting.KeywordTopNumber, setting.AllowPOSList))
    data['议题关键词'] = data['关键词'].apply(choose_first_keyword_in_dictionary, args=(dictionary_comparison_table_topic,))
    data['叙事关键词'] = data['关键词'].apply(choose_first_keyword_in_dictionary, args=(dictionary_comparison_table_topic,))
    data.to_pickle(get_new_path(DataFilePath, '关键词'))
