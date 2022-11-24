import sys
from loguru import logger

LOGGER_LEVEL = "DEBUG"
MinLengthOfWord = 2
KeywordTopNumber = 10
StopWordPath = 'setting/stopwords.txt'
ExtraDictionaryPath = 'setting/dict.txt'
IDFFilePath = 'setting/idf.txt'
AllowPOSList = ['n','nz','vn']

# 预设工具
def set_logger():
    logger.remove()
    logger.add(sys.stderr, level=LOGGER_LEVEL)
    return logger