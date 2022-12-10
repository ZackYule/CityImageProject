import pandas as pd
from utils import *

DictionaryFilePath = 'data/西安城市形象编码词表.pkl'
DataFilePath = 'data/西安城市形象数据_关键词.pkl'

if __name__ == "__main__":
    # 数据读取
    dictionary_comparison_table = pd.read_pickle(DictionaryFilePath)
    data = pd.read_pickle(DataFilePath)
    
    # 数据处理（多标签）
    # data = get_classification(data, '关键词', dictionary_comparison_table, inplace=True)

    # 数据处理（单标签）
    dictionary_comparison_table_topic = dictionary_comparison_table.drop(['积极判断框架','消极判断框架','事件框架','细节框架'], axis=1)
    dictionary_comparison_table_narration = dictionary_comparison_table[['积极判断框架','消极判断框架','事件框架','细节框架']]
    data = get_single_classification(data, '议题关键词', dictionary_comparison_table_topic, inplace=True)
    data = get_single_classification(data, '叙事关键词', dictionary_comparison_table_narration, inplace=True)

    # 数据保存
    data.to_pickle(get_new_path(DataFilePath, '议题分类'))