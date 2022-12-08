#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from utils import *

# ### 全局参数
DictionaryFilePath = 'data/西安城市形象编码词表.pkl'
DataFilePath = 'data/西安城市形象数据_关键词_议题分类.pkl'

if __name__ == "__main__":
    # ## 数据读取
    dictionary_comparison_table = pd.read_pickle(DictionaryFilePath)
    data = pd.read_pickle(DataFilePath)

    # ### 总数统计
    dictionary_statistics_df = pd.DataFrame()

    dictionary_statistics_df = get_class_sum(
        dictionary_comparison_table.columns, dictionary_statistics_df, data)

    for pt in ['豆瓣', '微博', '知乎']:
        dictionary_statistics_df = get_class_sum(
            dictionary_comparison_table.columns,
            dictionary_statistics_df,
            data,
            field='平台',
            filter_content=pt)

    # ## 数据展示
    data_to_show = dictionary_statistics_df
    data_to_show

    # ## 数据保存
    data_to_save = dictionary_statistics_df
    OutFilePath = get_new_path(DictionaryFilePath, '数量分布')
    data_to_save.to_pickle(OutFilePath)