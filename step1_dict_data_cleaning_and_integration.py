import pandas as pd
from utils import *

DictFilePath = 'data/编码框架及关键词列表.xlsx'
OutDictFilePath = 'data/西安城市形象编码词表.pkl'

if __name__ == "__main__":
    # 数据读取
    topic_data = pd.read_excel(DictFilePath)
    narration_data = pd.read_excel(DictFilePath, sheet_name=1)

    # 数据处理
    # ## 汇总
    topic_data['编码类型'] = '议题编码'
    narration_data['编码类型'] = '叙事编码'
    topic_data.columns = narration_data.columns = ['一级框架类型','二级框架类型','框架说明', '框架关键词', '编号', '类型']
    dictionary_data = pd.concat([topic_data[1:], narration_data[1:]], axis=0).reset_index(drop=True)
    # ## 分词
    dictionary_comparison_table = pd.DataFrame()
    for index, class_name in dictionary_data['二级框架类型'].items():
        dictionary_comparison_table[class_name] = pd.Series(safe_cut_words(dictionary_data.loc[index,'框架关键词'], '、'))

    # 数据保存
    dictionary_comparison_table.to_pickle(OutDictFilePath)