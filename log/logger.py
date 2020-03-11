#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/21'
# @description:


import os
from os.path import exists
import logging
import logging.config


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
    def load_configure(config_file=''):
        # 通过os.chdir()可以动态改变工作目录，改变log/app.log文件生成位置
        log_dir = os.path.join(os.getcwd(), 'log')
        if not exists(log_dir):
            os.mkdir(log_dir)
        if config_file:
            print("Set log configure file is: " + config_file)
            logging.config.fileConfig(config_file)
        else:
            print("Default log configure file is: " + CONF_FILE)
            logging.config.fileConfig(CONF_FILE)

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
