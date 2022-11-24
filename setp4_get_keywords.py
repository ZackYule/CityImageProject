import pandas as pd
import jieba.analyse as analyse
import setting

DataFilePath = 'data/西安城市形象数据.pkl'
IDFFilePath = 'setting/idf.txt'


def get_key_word_from_a_doc(content, topK=10):
    return ' '.join(analyse.extract_tags(content, topK))


if __name__ == "__main__":
    data = pd.read_pickle(DataFilePath)
    data = data.sample(10)
    analyse.set_idf_path(IDFFilePath)
    data['关键词'] = data['内容'].apply(get_key_word_from_a_doc, args=(setting.KeywordTopNumber,))
    print(data['关键词'])
