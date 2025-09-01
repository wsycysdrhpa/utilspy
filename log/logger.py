#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/21'
# @description:


import os
from os.path import exists
import logging
import logging.config
import tempfile
import configparser


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

# log configuration file absoluate path
CONF_FILE = os.path.join(CURRENT_DIR_PATH, 'conf/logger.ini')


class Logger(object):

    instance = None

    def __init__(self):
        # 默认的root logger
        self._logger = logging.getLogger()
        # 存储不同名字的logger, 不包括root logger
        self._logger_dict = {}

    @staticmethod
    def get_instance():
        if not Logger.instance:
            Logger.instance = Logger()
        return Logger.instance

    def get_logger(self, logger_name=None):
        if not logger_name:
            return self._logger
        else:
            if logger_name not in self._logger_dict:
                self._logger_dict[logger_name] = logging.getLogger(logger_name)
            return self._logger_dict[logger_name]

    @staticmethod
    def load_configure(config_file='', port=None, pid=None):
        """
        加载日志配置
        Args:
            config_file: 配置文件路径
            port: 服务端口号，用于生成日志文件名
            pid: 进程号，用于生成日志文件名
        """
        # 通过os.chdir()可以动态改变工作目录，改变log/app.log文件生成位置
        log_dir = os.path.join(os.getcwd(), 'log')
        if not exists(log_dir):
            os.mkdir(log_dir)

        # 确定使用的配置文件
        if config_file:
            actual_config_file = config_file
            print("Set log configure file is: " + config_file)
        else:
            actual_config_file = CONF_FILE
            print("Default log configure file is: " + CONF_FILE)

        # 如果需要动态生成日志文件名
        if port is not None or pid is not None:
            Logger._load_configure_with_dynamic_path(actual_config_file, port, pid)
        else:
            logging.config.fileConfig(actual_config_file)

    @staticmethod
    def _load_configure_with_dynamic_path(config_file, port=None, pid=None):
        """
        使用动态路径加载日志配置
        """
        # 读取原始配置文件
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        # 生成动态日志文件名
        if port is not None:
            log_filename = f'app_port_{port}.log'
        elif pid is not None:
            log_filename = f'app_pid_{pid}.log'
        else:
            log_filename = 'app.log'

        # 更新配置文件中的日志文件路径
        for section in config.sections():
            if section.startswith('handler_'):
                if 'args' in config[section]:
                    args_str = config[section]['args']
                    # 解析args字符串，替换日志文件路径
                    if 'log/app.log' in args_str:
                        new_args = args_str.replace('log/app.log', f'log/{log_filename}')
                        config[section]['args'] = new_args

        # 创建临时配置文件
        temp_config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False, encoding='utf-8')
        config.write(temp_config_file)
        temp_config_file.close()

        # 使用临时配置文件加载日志配置
        logging.config.fileConfig(temp_config_file.name)

        # 删除临时配置文件
        os.unlink(temp_config_file.name)

        print(f"Dynamic log file: log/{log_filename}")

    @staticmethod
    def debug(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).debug(message)
        else:
            Logger.get_instance().get_logger().debug(message)

    @staticmethod
    def info(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).info(message)
        else:
            Logger.get_instance().get_logger().info(message)

    @staticmethod
    def warning(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).warning(message)
        else:
            Logger.get_instance().get_logger().warning(message)

    @staticmethod
    def error(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).error(message)
        else:
            Logger.get_instance().get_logger().error(message)

    @staticmethod
    def critical(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).critical(message)
        else:
            Logger.get_instance().get_logger().critical(message)


if __name__ == "__main__":
    pass
    Logger.load_configure()

    # 以下代码输出文件名字、行数等信息时有问题，都是：logger.py[line:44]
    # Logger.debug(u'hello', logger_name='dual')
    # Logger.info(u'hello', logger_name='dual')
    # Logger.warning(u'hello', logger_name='dual')
    # Logger.error(u'hello', logger_name='dual')
    # Logger.critical(u'hello', logger_name='dual')

    # logger = logging.getLogger()
    logger = logging.getLogger('dual')
    logger.debug('你好')
    logger.info('hello')
    logger.warning('你好')
    logger.error('hello')
    logger.critical('你好')

    # logger = logging.getLogger('rotatingFileDual')
    # for i in range(100):
    #     logger.debug('你好')
    #     logger.info('hello')
    #     logger.warning('你好')
    #     logger.error('hello')
    #     logger.critical('你好')
