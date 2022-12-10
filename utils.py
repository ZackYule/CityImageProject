# ## 函数工具
import os
import re
import pandas as pd
import jieba
import jieba.posseg as psg
import cn2an
import setting

logger = setting.set_logger()


# 生成新路径，用来保存修改后文件
def get_new_path(old_path, new_tag):
    path_list = old_path.rsplit('.', 1)
    path_list[0] += '_' + new_tag
    return '.'.join(path_list)


# 去除异常符号清洗
def remove_abnormal_symbols(content):
    res = re.sub('\xb4|\u200b|٩|`|Д|۶|๓|╰|╯|♡|◦|˙|ò|ᆺ|ó|➕|•̥́|ˍ|•̀ू|✂|✪|▽', '',
                 str(content))
    return res


# 富文本清洗
def rich_text_to_normal(content):
    # 删除html文本
    content = re.sub('<[^<]+?>', '', str(content)).replace('\n', '').strip()
    # 删除文本中的网址
    content = re.sub(r'https://[a-zA-Z0-9.?/&=:]*', '', content)
    content = re.sub(r'http://[a-zA-Z0-9.?/&=:]*', '', content)
    return content


# 去除汉字
def remove_chinese_characters(content):
    content = re.sub('[\u4e00-\u9fa5]', '', content).strip()
    return content


# 时间选取
def search_time_string(content):
    match = re.search(
        '\d{4}-\d{1,2}-\d{1,2}\s*\d{0,2}(:\d{1,2})?(:\d{1,2})?(\.\d{1,9})?',
        content)
    if match:
        return pd.Timestamp(match.group())
    else:
        return pd.NaT


# 数字清洗（整数）
def get_number_from_string(content):
    if (not content) or pd.isnull(content) or pd.isna(content):
        return 0
    content = ''.join(
        re.findall(
            r"零|壹|貳|參|肆|伍|陸|柒|捌|玖|拾|念|佰|仟|〇|一|二|三|四|五|六|七|八|九|十|廿|百|千|万|亿|\d+",
            str(content)))
    # 解决上一步得到空字符串引发的bug toDO: 非最佳方法
    if (not content) or pd.isnull(content) or pd.isna(content):
        return 0
    try:
        content_num = cn2an.cn2an(content, 'smart')
    except Exception as err:
        logger.debug(
            f'🤡识别中文数字时ERROR!!--->{err=}, {type(err)=}, content:{content}')
        content_num = pd.NA
    return content_num


# 分词工具
def chinese_word_cut(my_text,
                     min_length_of_word=2,
                     stop_word_path=None,
                     extra_dictionary_path=None,
                     flag_list=['n', 'nz', 'vn']):
    # 设置扩展字典
    if os.path.exists(extra_dictionary_path):
        jieba.load_userdict(extra_dictionary_path)
        jieba.initialize()
    else:
        logger.info(f'扩充字典不存在{extra_dictionary_path}')
    # 设置停用词字典
    if os.path.exists(stop_word_path):
        try:
            stopwords_list_unprocessed = open(stop_word_path, encoding='utf-8')
            stop_word_list = []
            for line in stopwords_list_unprocessed:
                line = re.sub(u'\n|\\r', '', line)
                stop_word_list.append(line)
        except:
            stop_word_list = []
            logger.debug("error in stop_file")
    else:
        logger.info(f'停用词典不存在{stop_word_path}')

    # jieba分词
    word_list = []
    seg_list = psg.cut(my_text)
    for seg_word in seg_list:
        # word = re.sub(u'[^\u4e00-\u9fa5]','',seg_word.word) # 去除英文
        word = seg_word.word
        is_unfit = False
        for stop_word in stop_word_list:  # this word is stop word
            if stop_word == word or len(word) < min_length_of_word:
                is_unfit = True
                break
        if (not is_unfit) and seg_word.flag in flag_list:
            word_list.append(word)
    return (" ").join(word_list)


# 手动安全分词
def safe_cut_words(words_str, seg=' '):
    if not seg:
        return
    if not isinstance(words_str, str):
        logger.error(f'手动安全分词输入值不是str，而是{words_str}')
        words_str = str(words_str)
    words_str = re.sub(f'[{seg}]+', '|', words_str).strip('|')
    if not words_str:
        return
    return words_str.split('|')


# 列表重合检测
def list_detection(list1, list2) -> bool:
    return frozenset(list1).intersection(list2)


# 词典检测  返回是否属于其分类，并返回重合词
def dictionary_detection(words_str, dic_df, dictionary_column_name, seg=' '):
    word_list = safe_cut_words(words_str, seg)
    if not word_list:
        return 0, ''

    keywords_list = dic_df[dic_df[dictionary_column_name].notna(
    )][dictionary_column_name].to_list()

    logger.debug(word_list)
    coincident_keyword_set = list_detection(word_list, keywords_list)

    if len(coincident_keyword_set) > 0:
        return 1, ' '.join(coincident_keyword_set)

    return 0, ''


# 类别检测  返回是否属于其分类，并返回重合词
def class_detection(words_str, dic_df, seg=' '):
    for class_name in dic_df.columns:
        is_class, target_word = dictionary_detection(words_str,
                                                     dic_df,
                                                     class_name,
                                                     seg=' ')
        if is_class:
            return class_name
    return ''


# 有效关键词检测
def choose_first_keyword_in_dictionary(words_str,
                                       dictionary_comparison_table,
                                       seg=' '):
    word_list = safe_cut_words(words_str, seg)
    if not word_list:
        return ''
    for word in word_list:
        if word in dictionary_comparison_table.values:
            return word
    return ''


# pandas 获取分类（一整列数据的全部分类及选中词）
def get_classification(data_df, data_words_column_name, dic_df, inplace=False):
    res_df = pd.DataFrame()
    for class_name in dic_df.columns:
        res_df = pd.concat(
            (res_df,
             apply_and_concat_data_frame(
                 data_df,
                 data_words_column_name,
                 dictionary_detection,
                 args=(dic_df, class_name),
                 column_names=[class_name, class_name + '选中词'])),
            axis=1)
    if inplace:
        return pd.concat((data_df, res_df), axis=1)
    return res_df


# pandas 单标签分类（一整列数据的全部分类及选中词）
def get_single_classification(data_df,
                              data_words_column_name,
                              dic_df,
                              inplace=False):
    res_df = pd.DataFrame()
    res_df[data_words_column_name +
           '分类'] = data_df[data_words_column_name].apply(class_detection,
                                                         args=(dic_df, ))

    if inplace:
        return pd.concat((data_df, res_df), axis=1)
    return res_df


# pandas 一列生成多列
def apply_and_concat_data_frame(df,
                                field,
                                func,
                                args,
                                column_names,
                                inplace=False):
    if inplace:
        return pd.concat((df, df[field].apply(
            lambda cell: pd.Series(func(cell, *args), index=column_names))),
                         axis=1)
    else:
        return df[field].apply(
            lambda cell: pd.Series(func(cell, *args), index=column_names))


# pandas 清洗一列数字并修改格式
def clean_number_of_data_frame(df, column_names, inplace=False):

    def helper(df, column_name, inplace=inplace):
        if inplace:
            df[column_name] = df[column_name].apply(
                get_number_from_string).fillna(0).astype('Int64')
        else:
            return df[column_name].apply(get_number_from_string).fillna(
                0).astype('Int64')

    if isinstance(column_names, list):
        if inplace:
            for column_name in column_names:
                helper(df, column_name, inplace=True)
        else:
            new_df = pd.DataFrame()
            for column_name in column_names:
                new_df[column_name] = helper(df, column_name)
            return new_df
    else:
        return helper(df, column_names, inplace=inplace)


# pandas 分词函数
def get_segmentation_words_from_data_frame(
        data,
        content_column_name,
        new_column_name,
        inplace=False,
        min_length_of_word=setting.MinLengthOfWord,
        stop_word_path=setting.StopWordPath,
        extra_dictionary_path=setting.ExtraDictionaryPath,
        flag_list=setting.AllowPOSList):
    min_length_of_word = int(min_length_of_word)
    if inplace:
        data[new_column_name] = data[content_column_name].apply(
            chinese_word_cut,
            args=(min_length_of_word, stop_word_path, extra_dictionary_path,
                  flag_list))
    else:
        return data[content_column_name].apply(
            chinese_word_cut,
            args=(min_length_of_word, stop_word_path, extra_dictionary_path,
                  flag_list))


# pandas 时间切分
def time_cut(df, time_column_name, freq_count=1, freq_tag='M'):
    # 获取切割标签
    if freq_count:
        if freq_count == 1:
            freq_str = freq_tag
        else:
            freq_str = str(freq_count) + freq_tag
    # 判断切割单位（按天/按月）
    if freq_tag == 'D':
        bins = pd.date_range(
            start=pd.datetime.date(df['发布时间'].iloc[0]),
            end=pd.datetime.date(df['发布时间'].iloc[-1] +
                                 pd.DateOffset(days=freq_count)),
            freq=freq_str)
    elif freq_tag == 'M' or freq_tag == 'MS':
        bins = pd.date_range(
            start=pd.datetime.strftime(df['发布时间'].iloc[0], '%Y-%m'),
            end=pd.datetime.strftime(
                df['发布时间'].iloc[-1] + pd.DateOffset(months=freq_count),
                '%Y-%m'),
            freq=freq_str)
        logger.debug(freq_str)
        logger.debug(bins)
    else:
        logger.error(f'切分单位错位：{freq_tag}')
        return
    df.loc[:, f'{time_column_name}_group'] = pd.cut(df[time_column_name],
                                                    bins,
                                                    right=False)
    return df


# pandas 获取分组统计数（不同app下）
def get_app_group_counts(df_data,
                         group_name,
                         app_name=None,
                         column_name=None,
                         is_fill_zero=False):
    if app_name:
        res_series = df_data[df_data['平台'] == app_name].groupby(
            group_name).agg('count').iloc[:, 0].astype('Int64')
    else:
        res_series = df_data.groupby(group_name).agg(
            'count').iloc[:, 0].astype('Int64')
    if column_name:
        res_series.name = column_name
    if is_fill_zero:
        res_series = res_series.fillna('0')
    return res_series


# pandas 获取平台点赞数分组统计（或其他任意数字）
def get_app_sum_counts(df_data,
                       group_name,
                       sum_target_volume_name='点赞数',
                       app_name=None):
    if not app_name:
        return df_data.loc[:, [sum_target_volume_name, group_name]].groupby(
            group_name).agg('sum', numeric_only=False).astype('Int64')
    return df_data[df_data['平台'] ==
                   app_name].loc[:,
                                 [sum_target_volume_name, group_name]].groupby(
                                     group_name).agg(
                                         'sum',
                                         numeric_only=False).astype('Int64')


# pandas 获取总数，直接保存至原表中
def get_class_sum(class_list, target_df, data, field=None, filter_content=''):
    # 保存列名
    target_column = filter_content + '总数'

    if field and filter_content:
        for column in class_list:
            target_df.loc[column, target_column] = data[
                data[field] == filter_content][column].sum()
    elif not field or not filter_content:
        for column in class_list:
            target_df.loc[column, target_column] = data[column].sum()
    else:
        logger.error(
            f'没有指定过滤列名称,field:{field},filter_content:{filter_content}')

    target_df[target_column] = target_df[target_column].astype('Int64')
    return target_df


if __name__ == "__main__":
    try:
        print(pd.Timestamp('2022-1-18  12 23'))
    except:
        print('error')
    print(search_time_string('2022-1-18  12 23'))
    DataFilePath = 'data/西安城市形象数据_关键词_关键词选取.pkl'
    DictionaryFilePath = 'data/西安城市形象编码词表.pkl'
    data = pd.read_pickle(DataFilePath).sample(10).reset_index(drop=True)
    dictionary_comparison_table = pd.read_pickle(DictionaryFilePath)
    print(
        get_single_classification(data,
                                  '议题关键词',
                                  dictionary_comparison_table,
                                  inplace=False))
