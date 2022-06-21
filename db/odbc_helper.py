# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '2016/2/19'


import logging
from _sqlite3 import ProgrammingError, IntegrityError

import pyodbc

LOGGER = logging.getLogger("dual")


class OdbcHelper(object):
    # pyodbc: sql语句注入参数，使用"?"作为占位符
    def __init__(self, dsn=None):
        self._conn = None
        if dsn:
            self.open(dsn)
        pass

    def open(self, dsn):
        self._conn = pyodbc.connect(dsn)

    def read(self, sql, params=None):
        cursor = self._conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def yield_read(self, sql, params=None):
        cur = self._conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        result = cur.fetchone()
        while result:
            yield result
            result = cur.fetchone()
        cur.close()

    def execute(self, sql, params=None):
        cursor = self._conn.cursor()
        sql_info = str(sql) + "\t" + str(params)
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            cursor.commit()
        except ProgrammingError, e:
            LOGGER.error("执行sql失败：" + e.message + "\tsql=" + sql_info)
        except IntegrityError, e:
            LOGGER.error("执行sql失败IntegrityError：" + e.message + "\tsql=" + sql_info)
        except Exception, e:
            LOGGER.error("执行sql失败 未知错误：" + e.message + "\tsql=" + sql_info)

    def execute_many(self, sql, params_list=None):
        if not params_list:
            LOGGER.error("params_list is None")
        cursor = self._conn.cursor()
        try:
            cursor.executemany(sql, params_list)
            cursor.commit()
        except ProgrammingError, e:
            LOGGER.error("执行sql失败：" + e.message + str(params_list[0]))
        except IntegrityError, e:
            LOGGER.error("执行sql失败IntegrityError：" + e.message + str(params_list[0]))
        except Exception, e:
            LOGGER.error("执行sql失败 未知错误：" + e.message + str(params_list[0]))

    def close(self):
        self._conn.close()


if __name__ == "__main__":
    pass
    # TODO pyodbc 可以连接mysql, sql server, access, 考虑写一个通用的helper，支持连接这三种database
    # 都是sql类的，所以连接参数用一个str
    # 其他方法一样
    data_source_file = "../data/news.mdb"
    dsn = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % data_source_file
    dsn = "Driver={MySQL ODBC 5.1 Driver};Server=10.10.10.123;Port=3306;Database=music_knowledge;User=dev;Password=kaimen;"
    db_helper = OdbcHelper(dsn)
    result = db_helper.read("select * from style")
    # for record in result:
    #     print record
    for record in result:
        print record
