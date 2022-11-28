import pandas as pd
from utils import *

DictionaryFilePath = 'data/西安城市形象编码词表.pkl'
DataFilePath = 'data/西安城市形象数据_关键词.pkl'

if __name__ == "__main__":
    # 数据读取
    dictionary_comparison_table = pd.read_pickle(DictionaryFilePath)
    data = pd.read_pickle(DataFilePath)

    # 数据处理
    data = get_classification(data, '关键词', dictionary_comparison_table, inplace=True)

    # 数据保存
    data.to_pickle(get_new_path(DataFilePath, '议题分类'))