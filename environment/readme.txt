配置项目运行环境，加载总配置文件，总配置文件可参考conf/ref.ini
总配置文件命名为: {调用脚本前缀}.ini
如：
调用脚本: main.py
总配置文件命名: main.ini


若总配置文件中有如下log配置项，则加载新的log配置文件，新log配置文件放置在：{working_dir}/conf/{execute_script_name}.ini
若总配置文件中没有log配置项，则加载默认log配置文件;
调用Environment.get_instance().init()方法进行配置，log/app.log文件的生成位置不会改变，总是{工程目录}/log/app.log;
除了可以配置日志外，还可以配置数据库等其他选项;
[logger]
name ={execute_script_name}.ini


# 使用方法
import os
import logging

from utilspy.environment.environment import Environment

LOGGER = logging.getLogger('dual')

CURRENT_FILE_PATH = os.path.abspath(__file__)

Environment.get_instance(load_configure=False).init(CURRENT_FILE_PATH, 1)

LOGGER.debug(u'hello')
LOGGER.info(u'hello')
LOGGER.warning(u'hello')
LOGGER.error(u'hello')
LOGGER.critical(u'hello')
