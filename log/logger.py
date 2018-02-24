#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/21'
# @description:


import os
import logging
import logging.config


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)
PARENT_DIR_PATH = os.path.dirname(CURRENT_DIR_PATH)

# Dict absoluate path
CONF_FILE = os.path.join(CURRENT_DIR_PATH, 'conf/logger.conf')


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
    def load_configure(config_file=None):
        if config_file:
            print config_file
            logging.config.fileConfig(config_file)
        else:
            print CONF_FILE
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

    logger = logging.getLogger()
    # logger = logging.getLogger('dual')
    logger.debug(u'hello')
    logger.info(u'hello')
    logger.warning(u'hello')
    logger.error(u'hello')
    logger.critical(u'hello')
