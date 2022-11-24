# ## 函数工具
import re
import pandas as pd
import cn2an
import setting
logger = setting.set_logger()

# 生成新路径，用来保存修改后文件
def get_new_path(old_path, new_tag):
    path_list = old_path.rsplit('.', 1)
    path_list[0] += '_'+new_tag
    return '.'.join(path_list)

# 去除异常符号清洗
def remove_abnormal_symbols(content):
    res = re.sub('\xb4|\u200b|٩|`|Д|۶|๓|╰|╯|♡|◦|˙|ò|ᆺ|ó|➕|•̥́|ˍ|•̀ू|✂|✪|▽', '', str(content))
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
    match = re.search('\d{4}-\d{1,2}-\d{1,2}\s*\d{0,2}(:\d{1,2})?(:\d{1,2})?(.\d{1,9})?', content)
    if match:
        return pd.Timestamp(match.group())
    else:
        return pd.NA

# 数字清洗（整数）
def get_number_from_string(content):
    if (not content) or pd.isnull(content) or pd.isna(content):
        return 0
    content = ''.join(re.findall(r"零|壹|貳|參|肆|伍|陸|柒|捌|玖|拾|念|佰|仟|〇|一|二|三|四|五|六|七|八|九|十|廿|百|千|万|亿|\d+",str(content)))
    try:
        content_num = cn2an.cn2an(content, 'smart')
    except Exception as err:
        logger.debug(f'🤡ERROR!!--->{err=}, {type(err)=}')
        content_num = pd.NA
    return content_num

# pandas 一列生成多列
def apply_and_concat(df, field, func, args, column_names):
    return pd.concat((
        df,
        df[field].apply(
            lambda cell: pd.Series(func(cell, *args), index=column_names))), axis=1)

# pandas 清洗一列数字并修改格式
def clean_number_of_data_frame(df, column_names, inplace=False):
    def helper(df, column_name, inplace=inplace):
        if inplace:
            df[column_name] = df[column_name].apply(get_number_from_string).fillna(0).astype('Int64')
        else:
            return df[column_name].apply(get_number_from_string).fillna(0).astype('Int64')
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


if __name__ == "__main__":
    try:
        print(pd.Timestamp('2022-1-18  12 23'))
    except:
        print('error')
    print(search_time_string('2022-1-18  12 23'))