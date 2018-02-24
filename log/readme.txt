若使用默认的配置文件conf/logger.conf
相对调用logger.warning()等方法的文件，需要先具有../log/的目录
调用才可以输出到log/app.log中

调用方法：
import logging

from utilspy.log.logger import Logger

Logger.load_configure()

# 只输出到屏幕
logger = logging.getLogger()

# 同时输出到屏幕和文件
logger = logging.getLogger('dual')

logger.debug(u'hello')
logger.info(u'hello')
logger.warning(u'hello')
logger.error(u'hello')
logger.critical(u'hello')
