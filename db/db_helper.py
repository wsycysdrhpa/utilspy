# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-9-16'


import ConfigParser

from utilspy.db.mysql_helper import MySqlHelper


class DbHelper(MySqlHelper):
    def __init__(self, db_section_name, configure_file_name):
        MySqlHelper.__init__(self)
        self.open_by_conf(db_section_name, configure_file_name)
        pass

    def open_by_conf(self, db_section_name, configure_file_name):
        db_setting = self._load_db_settings(db_section_name, configure_file_name)
        db = self.open(db_setting["server"], db_setting["db"], db_setting["user"], db_setting["password"])
        return db

    def _load_db_settings(self, db_section_name, configure_file_name):
        config = ConfigParser.ConfigParser()
        settings = {}
        with open(configure_file_name, "r") as configFile:
            config.readfp(configFile)
            settings["db"] = config.get(db_section_name, "db")
            settings["server"] = config.get(db_section_name, "host")
            settings["user"] = config.get(db_section_name, "user")
            settings["password"] = config.get(db_section_name, "passwd")
        return settings


if __name__ == "__main__":
    pass
