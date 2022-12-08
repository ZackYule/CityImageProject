from utils import *

OutFilePath = 'data/西安城市形象数据.pkl'

if __name__ == "__main__":

    # 微博
    weibo = pd.read_csv("data/西安微博.csv")
    weibo.rename(columns={'微博正文': '内容', 'user_id': 'user_tag'}, inplace=True)
    weibo = weibo[['user_tag', '内容', '转发数', '评论数', '点赞数', '发布时间']]
    weibo['平台'] = '微博'

    weibo_add = pd.read_csv("data/西安微博补充.csv")
    weibo_add.rename(columns={
        '微博正文': '内容',
        'user_id': 'user_tag'
    },
                     inplace=True)
    weibo_add = weibo_add[['user_tag', '内容', '转发数', '评论数', '点赞数', '发布时间']]
    weibo_add['平台'] = '微博'

    # 知乎
    zhihu = pd.read_csv("data/西安回答详情.csv")
    zhihu.rename(columns={
        'answer_content': '内容',
        'publish_time': '发布时间',
        'voters_num': '点赞数',
        'comments_num': '评论数',
        'author_url': 'user_tag'
    },
                 inplace=True)
    zhihu = zhihu[['内容', '发布时间', '点赞数', '评论数', 'user_tag']]
    zhihu['发布时间'] = zhihu['发布时间'].apply(search_time_string)
    zhihu['平台'] = '知乎'

    # 豆瓣
    douban = pd.read_csv("data/豆瓣日记内容.csv")
    douban['内容'] = douban['标题'] + douban['内容']
    douban.rename(columns={'作者主页': 'user_tag', '喜欢数': '点赞数'}, inplace=True)
    douban = douban[['内容', '发布时间', '点赞数', '收藏数', '转发数', 'user_tag']]
    douban['平台'] = '豆瓣'

    # 数据集合处理
    data = pd.concat([douban, weibo, zhihu, weibo_add], axis=0)
    data = data.applymap(remove_abnormal_symbols)
    data[['内容']] = data[['内容']].applymap(rich_text_to_normal)
    data[['发布时间']] = data[['发布时间']].applymap(search_time_string)
    data['发布时间月份'] = data['发布时间'].dt.strftime('%Y-%m')
    clean_number_of_data_frame(data, ['点赞数', '收藏数', '转发数', '评论数'], True)
    data.reset_index(drop=True, inplace=True)

    # 保存数据
    data.to_pickle(OutFilePath)