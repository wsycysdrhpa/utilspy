配置项目运行环境，加载配置文件（2021.11.11后支持加载多个配置文件，配置文件通过列表传递进来）;
总配置文件可参考conf/ref.ini, 该文件默认不会加载，只是为了参考;
如果不指定配置文件, 默认总配置文件命名为: {调用脚本前缀}.ini（如果文件不存在，则默认加载 main.ini）
如：
调用脚本: main.py
总配置文件命名: main.ini

如果需要指定一个或多个配置文件, 都需要通过列表传递给conf_path_list:



若总配置文件中有如下log配置项，则加载新的log配置文件，新log配置文件放置在：{working_dir}/conf/{log_conf_file_name}.ini
若总配置文件中没有log配置项，则加载默认log配置文件;
调用Environment.get_instance().init()方法进行配置，load_user_configure表示是否加载用户总配置文件;
若需要加载新的log配置文件，则必须先加载总配置文件，从中进行设定;
log/app.log文件的生成位置不会改变，总是{工程目录}/log/app.log;
除了可以配置日志外，还可以配置数据库等其他选项;
[logger]
name ={log_conf_file_name}.ini



# 使用方法
import os
import logging

from utilspy.environment.environment import Environment

LOGGER = logging.getLogger('dual')

CURRENT_FILE_PATH = os.path.abspath(__file__)

Environment.get_instance(load_user_configure=False).init(CURRENT_FILE_PATH, 1)

LOGGER.debug(u'hello')
LOGGER.info(u'hello')
LOGGER.warning(u'hello')
LOGGER.error(u'hello')
LOGGER.critical(u'hello')
