import sys
from loguru import logger

LOGGER_LEVEL = "INFO"
MinLengthOfWord = 2        # 分词的最小字数
KeywordTopNumber = 10       # 最大关键字字数
StopWordPath = 'setting/stopwords.txt'
ExtraDictionaryPath = 'setting/dict.txt'
IDFFilePath = 'setting/idf.txt'
AllowPOSList = ['n','nz','vn']

# 预设工具
def set_logger():
    logger.remove()
    logger.add(sys.stderr, level=LOGGER_LEVEL)
    return logger