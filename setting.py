import sys
from loguru import logger

LOGGER_LEVEL = "DEBUG"


# 预设工具
def set_logger():
    logger.remove()
    handler_id = logger.add(sys.stderr, level=LOGGER_LEVEL)
    return logger