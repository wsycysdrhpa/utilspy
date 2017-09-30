# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import os
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError

from yzs_utils.logger import Logger


class Environment():

    instance = None

    def __init__(self):
        self._working_path = ""
        self._app_name = ""

    @staticmethod
    def get_instance():
        if not Environment.instance:
            Environment.instance = Environment()
        return Environment.instance

    def init_by_file_name(self, start_file_path, start_file_name, start_file_depth=1):
        start_file_name = os.path.join(start_file_path, start_file_name)
        self.init(start_file_name, start_file_depth)

    def init(self, start_file_name, start_file_depth):

        """
        初始化应用环境
        :param start_file_name:   调用本方法的代码文件的完整路径
        :param start_file_depth:  调用本方法的代码文件距离工作目录的深度。如果在工作目录下，深度为1；
                                  如果在工作目录的一级子文件夹下，深度为2， 以此类推。
        """
        self._working_path, self._app_name = self._parse_start_file_name(start_file_name, start_file_depth)
        self._set_working_path(self._working_path)

        self._init_logger()

        self._configure_parser = ConfigParser()
        self._is_configure_loaded = False
        self._load_configure()

    def get_db_setting(self, db_setting_section_name):
        db_setting = {"host": self.get_configure_value(db_setting_section_name, "host"),
                      "db": self.get_configure_value(db_setting_section_name, "db"),
                      "user": self.get_configure_value(db_setting_section_name, "user"),
                      "passwd": self.get_configure_value(db_setting_section_name, "passwd")}
        return db_setting

    def get_app_name(self):
        return self._app_name

    def get_working_path(self):
        return self._working_path

    def get_options(self, section):
        return self._configure_parser.options(section)

    def get_configure_value(self, section, key):
        try:
            value = self._configure_parser.get(section, key)
            return value
        except NoSectionError, e:
            Logger.error(e.message)
            return None

    def _parse_start_file_name(self, start_file_name, start_file_depth):

        """
        解析启动文件名称和该文件深度，返回程序工作目录和程序名称
        :param start_file_name:   调用本方法的代码文件的完整路径
        :param start_file_depth:  调用本方法的代码文件距离工作目录的深度。如果在工作目录下，深度为1；
                                  如果在工作目录的一级子文件夹下，深度为2， 以此类推。
        :return:
        """

        start_file_name = start_file_name.replace("\\", "/")
        file_name_parts = start_file_name.split('/')
        if not file_name_parts:
            Logger.error(u"启动文件输入参数错误，输入的不是完整的文件名: " + start_file_name)
            return

        app_name = file_name_parts[-1]
        if "." in app_name:
            app_name = app_name[:app_name.rindex(".")]

        file_name_parts = file_name_parts[:start_file_depth * -1]
        working_dir = os.sep.join(file_name_parts)
        return working_dir, app_name

    def set_configure_value(self, section, key, value):
        self._configure_parser.set(section, key, value)

    def _init_logger(self, logging_file_name="logging.conf"):
        log_file_whole_name = os.path.join(self._working_path, "conf", logging_file_name)
        print "log_configure_file = " + log_file_whole_name
        Logger.load_configure(log_file_whole_name)

    def _load_configure(self):
        configure_file_name = os.path.join(self._working_path, "conf", self._app_name + ".conf")
        if self._is_configure_loaded:
            return
        if not configure_file_name:
            return
        self._configure_parser.read(configure_file_name)

    def _set_working_path(self, work_path):
        os.chdir(work_path)
        print "working dir is : " + work_path


if __name__ == "__main__":
    pass