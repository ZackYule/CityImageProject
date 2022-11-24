
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


DataFilePath = 'data/西安城市形象数据_分词.pkl'
OutIDFFilePath = 'setting/idf_list.txt'

if __name__ == "__main__":
    data = pd.read_pickle(DataFilePath)
    # 选取词集
    corpus = data['分词'].to_list()
    # 统计idf
    tfidf_vector = TfidfVectorizer(use_idf=True, smooth_idf=True, norm=None, max_features=1000, max_df = 0.5, min_df = 10) # max_df = 0.05, min_df = 15
    tfidf_features = tfidf_vector.fit_transform(corpus)
    keywords = tfidf_vector.get_feature_names_out()
    # 构建idf词典
    idf_df_data = {'word':keywords}
    # idf_df_data = {'word':keywords,'idf':tfidf_vector.idf_}
    idf_df = pd.DataFrame(idf_df_data)
    idf_df.to_csv(OutIDFFilePath, header=None, index=None, sep=' ', mode='a')