from utils import *

DataFilePath = 'data/西安城市形象数据.pkl'


if __name__ == "__main__":
    data = pd.read_pickle(DataFilePath)
    get_segmentation_words_from_data_frame(data, '内容', '分词', inplace=True)
    data.to_pickle(get_new_path(DataFilePath, '分词'))