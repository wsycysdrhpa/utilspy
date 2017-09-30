# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import logging
from _sqlite3 import ProgrammingError, IntegrityError

import MySQLdb


logger = logging.getLogger("error")

class MySqlHelper(object):

    def __init__(self):
        self._conn = None

    def create_db(self, host, db_name, user, passwd):
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, charset="utf8")
        cursor = conn.cursor()
        cursor.execute('create database if not exists ' + db_name)
        conn.commit()

    def open(self, host, db_name, user, passwd):
        self._conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name, charset="utf8")
        return self._conn

    def open_by_db_setting(self, db_setting):
        return self.open(db_setting["host"], db_setting["db"], db_setting["user"], db_setting["passwd"])

    def read(self, sql, params=None):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchall()
        cur.close()
        return result

    def yield_read(self, sql, params=None):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        while True:
            result = cur.fetchone()
            if result is None:
                break
            yield result
        cur.close()

    def import_data_from_sql(self, sql_file_name):
        sql_file = open(sql_file_name, "r")
        sql = "".join(sql_file.readlines())
        sql_file.close()
        self.execute(sql)

    def execute(self, sql, params=None):
        cur = self._conn.cursor()
        sql_info = str(sql) + "\t" + str(params)
        try:
            cur.execute(sql, params)
            self._conn.commit()
        except ProgrammingError, e:
            logger.error("执行sql失败：" + e.message + "\tsql=" + sql_info)
        except IntegrityError, e:
            logger.error("执行sql失败IntegrityError：" + e.message + "\tsql=" + sql_info)
        except Exception, e:
            logger.error("执行sql失败 未知错误：" + e.message + "\tsql=" + sql_info)

    def execute_many(self, sql, params_list=None):
        if not params_list:
            logger.error("paramsList is None")
        cur = self._conn.cursor()
        try:
            cur.executemany(sql, params_list)
            self._conn.commit()
        except ProgrammingError, e:
            logger.error("执行sql失败：" + e.message + str(params_list[0]))
        except IntegrityError, e:
            logger.error("执行sql失败IntegrityError：" + e.message + str(params_list[0]))
        except Exception, e:
            logger.error("执行sql失败 未知错误：" + e.message + str(params_list[0]))

    def get_max_value(self, key_field_name, table_name):
        sql = "select max(" + key_field_name + ") from " + table_name
        result = self.read(sql)
        return result[0][0]

    def close(self):
        if self._conn:
            self._conn.close()

    def get_insert_id(self):
        return self._conn.insert_id()