默认使用的配置文件为：conf/logger.conf

调用方法：
# 注册过程
import os
import logging

from utilspy.log.logger import Logger

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

Logger.load_configure(CURRENT_DIR_PATH)

# 使用过程
# 只输出到屏幕
# logger = logging.getLogger()

# 同时输出到屏幕和文件
logger = logging.getLogger('dual')

logger.debug(u'hello')
logger.info(u'hello')
logger.warning(u'hello')
logger.error(u'hello')
logger.critical(u'hello')
