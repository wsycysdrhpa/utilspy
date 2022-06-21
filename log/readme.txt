默认使用的配置文件为：conf/logger.conf
若调用load_configure方法的脚本位置改变，则log/app.log文件的生成位置也会自动改变


调用方法：
import os
import logging

from utilspy.log.logger import Logger

# 注册过程
Logger.load_configure()

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
