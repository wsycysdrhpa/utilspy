# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '15-8-4'


import logging

import MySQLdb
from mysql.connector import ProgrammingError
from mysql.connector import IntegrityError
from mysql.connector.pooling import MySQLConnectionPool


LOGGER = logging.getLogger("dual")


class MySqlPoolHelper(object):
    def __init__(self, db_setting):
        self._pool = None
        self._init(db_setting)
        pass

    def create_db(self, host, db_name, user, passwd):
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, charset="utf8")
        cursor = conn.cursor()
        cursor.execute('create database if not exists ' + db_name)
        conn.commit()

    def read(self, sql, params=None):
        conn = self._pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def yield_read(self, sql):
        conn = self._pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        while True:
            result = cursor.fetchone()
            if result is None:
                break
            yield result
        cursor.close()
        conn.close()

    def execute(self, sql, params=None):
        conn = self._pool.get_connection()
        cursor = conn.cursor()
        sql_info = str(sql) + "\t" + str(params)
        try:
            cursor.execute(sql, params)
            conn.commit()
        except ProgrammingError, e:
            LOGGER.error("执行sql失败：" + e.message + "\tsql=" + sql_info)
        except IntegrityError, e:
            LOGGER.error("执行sql失败IntegrityError：" + e.message + "\tsql=" + sql_info)
        except Exception, e:
            LOGGER.error("执行sql失败 未知错误：" + e.message + "\tsql=" + sql_info)
        cursor.close()
        conn.close()

    def execute_many(self, sql, params_list=None):
        if not params_list:
            LOGGER.error("paramsList is None")
        conn = self._pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, params_list)
            conn.commit()
        except ProgrammingError, e:
            LOGGER.error("执行sql失败：" + e.message + str(params_list[0]))
        except IntegrityError, e:
            LOGGER.error("执行sql失败IntegrityError：" + e.message + str(params_list[0]))
        except Exception, e:
            LOGGER.error("执行sql失败 未知错误：" + e.message + str(params_list[0]))
        cursor.close()
        conn.close()

    def get_max_value(self, field_name, table_name):
        sql = "select max(%s) from %s" % (field_name, table_name)
        result = self.read(sql)
        return result[0][0]

    def get_insert_id(self):
        conn = self._pool.get_connection()
        insert_id = conn.insert_id()
        conn.close()
        return insert_id

    def close(self):
        self._pool._remove_connections()

    def _init(self, db_setting):
        # 如果是多线程公用一个连接池，那么，pool_size要大于thread_count
        # MySQLConnectionPool对pool_size的要求:0 <= pool_size <= 32
        pool_size = 5
        pool_name = None
        if db_setting.get("pool_size"):
            pool_size = int(db_setting["pool_size"])
            del db_setting["pool_size"]
        if db_setting.get("pool_name"):
            pool_name = db_setting["pool_name"]
            del db_setting["pool_name"]
        self._pool = MySQLConnectionPool(pool_size=pool_size, pool_name=pool_name, **db_setting)
        pass


if __name__ == "__main__":
    pass
