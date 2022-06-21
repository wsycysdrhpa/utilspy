#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/12'
# @description:


import os
import logging
from configparser import ConfigParser
from configparser import NoSectionError

from utilspy.log.logger import Logger


LOGGER = logging.getLogger('dual')


class Environment(object):

    instance = None

    def __init__(self, load_user_configure=False, conf_path_list=[]):
        self._configure_parser = ConfigParser()
        self._working_dir_path = ""
        self._script_name = ""
        self.load_user_configure = load_user_configure
        self._conf_path_list = conf_path_list

    @staticmethod
    def get_instance(load_user_configure=False, conf_path_list=[]):
        if not Environment.instance:
            Environment.instance = Environment(load_user_configure=load_user_configure, conf_path_list=conf_path_list)
        return Environment.instance

    def init(self, start_file_path, start_file_depth=1):
        """
        初始化应用环境
        :param start_file_path:   调用本方法的代码文件的完整路径
        :param start_file_depth:  调用本方法的代码文件距离工作目录的深度。如果在工作目录下，深度为1；
                                  如果在工作目录的一级子文件夹下，深度为2， 以此类推。
        """
        self._working_dir_path, self._script_name = self._parse_start_file_name(start_file_path, start_file_depth)
        self._set_working_path(self._working_dir_path)
        self._load_configure()
        self._init_logger()

    def get_script_name(self):
        return self._script_name

    def get_working_path(self):
        return self._working_dir_path

    def get_options(self, section):
        return self._configure_parser.options(section)

    def get_configure_value(self, section, key):
        try:
            value = self._configure_parser.get(section, key)
            return value
        except NoSectionError as e:
            LOGGER.error(e.message)
            return None

    # 必须是单例模式，self.get_db_setting('mysql')
    def get_db_setting(self, db_setting_section_name):
        db_setting = {
            "database": self.get_configure_value(db_setting_section_name, "database"),
            "host": self.get_configure_value(db_setting_section_name, "host"),
            "user": self.get_configure_value(db_setting_section_name, "user"),
            "password": self.get_configure_value(db_setting_section_name, "password")}
        return db_setting

    def set_configure_value(self, section, key, value):
        self._configure_parser.set(section, key, value)

    @staticmethod
    def _parse_start_file_name(start_file_path, start_file_depth):
        """
        解析启动文件名称和该文件深度，返回程序工作目录和调用脚本名称
        :param start_file_path:   调用本方法的代码文件的完整路径
        :param start_file_depth:  调用本方法的代码文件距离工作目录的深度。如果在工作目录下，深度为1；
                                  如果在工作目录的一级子文件夹下，深度为2， 以此类推。
        :return:
        """
        start_file_path = start_file_path.replace("\\", "/")
        file_name_parts = start_file_path.split('/')
        if not file_name_parts:
            LOGGER.error("启动文件输入参数错误，输入的不是完整的文件名: " + start_file_path)
            return None, None
        script_name = file_name_parts[-1]
        if "." in script_name:
            script_name = script_name[:script_name.rindex(".")]
        file_name_parts = file_name_parts[:start_file_depth*(-1)]
        project_dir = os.sep.join(file_name_parts)
        return project_dir, script_name

    def _init_logger(self):
        if not self.load_user_configure:
            Logger.load_configure()
            return
        try:
            logger_file_path = ""
            if self._configure_parser.has_option('logger', 'name'):
                logger_file_name = self._configure_parser.get('logger', 'name')
                logger_file_path = os.path.join(self._working_dir_path, "conf", logger_file_name)
            if os.path.exists(logger_file_path):
                Logger.load_configure(logger_file_path)
            else:
                Logger.load_configure()
        except NoSectionError as e:
            Logger.load_configure()
            LOGGER.warning(e.message)

    # 如果只有一个配置文件. 若需要加载总配置文件，总配置文件路径及命名如下:
    # {working_dir}/conf/{execute_script}.ini
    # 如果有多个配置文件, 则通过列表的形式传过来
    def _load_configure(self):
        if not self.load_user_configure:
            return
        if not self._conf_path_list:
            configure_file_path = os.path.join(self._working_dir_path, "conf", self._script_name + ".ini")
            if not os.path.exists(configure_file_path):
                self._script_name = "main"
                configure_file_path = os.path.join(self._working_dir_path, "conf", self._script_name + ".ini")
            print("Overall Configure file path is: %s" % configure_file_path)
            self._configure_parser.read(configure_file_path)
        else:
            print("Overall Configure file path is: %s" % self._conf_path_list)
            for conf_path in self._conf_path_list:
                self._configure_parser.read(conf_path)
            # sections = self._configure_parser.sections()
            # print(sections)
            # options = self._configure_parser.options("mysql")
            # print(options)

    @staticmethod
    def _set_working_path(work_dir_path):
        os.chdir(work_dir_path)
        print("Working dir is: %s" % work_dir_path)


if __name__ == "__main__":
    pass
    CURRENT_FILE_PATH = os.path.abspath(__file__)

    # 测试加载默认配置文件，只支持一个配置文件
    Environment.get_instance(load_user_configure=False).init(CURRENT_FILE_PATH, 3)

    # 测试加载自定义配置文件，支持一个或多个配置文件，都需要以列表的形式传递进来
    # conf_path_list = []
    # conf = r"D:\Code\Tools\Python\utilspy\environment\conf\ref.ini"
    # conf_2 = r"D:\Code\Tools\Python\utilspy\environment\conf\ref_2.ini"
    # conf_path_list.append(conf)
    # conf_path_list.append(conf_2)
    # Environment.get_instance(load_user_configure=True, conf_path_list=conf_path_list).init(CURRENT_FILE_PATH, 3)

    LOGGER.debug('hello')
    LOGGER.info('hello')
    LOGGER.warning('hello')
    LOGGER.error('hello')
    LOGGER.critical('hello')
