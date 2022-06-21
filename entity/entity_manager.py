#!/usr/bin/python
# -*- coding: utf8 -*-

# @author: 
# @date: '14-4-11'


from utilspy.db.mysql_helper import MySqlHelper


class EntityManager:
    def __init__(self):
        self._entity_dict = {}

    def build_dict(self, sql, db_section_name, key_index_list, entity_index_list):
        """
        根据输入键-值索引序列，对应sql语句中读取字段的的索引号建立字典
        key：
        若key_index_list长度为1，则直接以record[key_index_list[0]]为key
        若key_index_list长度大于1，则key为一个元组
        value：
        若entity_index_list长度为1，record[entity_index_list[0]]为value
        若entity_index_list长度大于1，value为一个list
        @param sql: sql语句
        @param db_section_name: 配置文件中数据库配置头
        @param key_index_list: 键 索引序列
        @param entity_index_list:值 索引序列
        """
        db_helper = MySqlHelper(db_section_name)
        record_list = db_helper.read(sql)
        for record in record_list:
            key_entity = []
            if len(key_index_list) == 1:
                key = record[key_index_list[0]]
                if type(key) == unicode:
                    key = key.encode("utf8")
            else:
                for index in key_index_list:
                    key_entity.append(record[index])
                key = tuple(key_entity)
            entity = []
            if len(entity_index_list) == 1:
                self._entity_dict[key] = record[entity_index_list[0]]
            else:
                for index in entity_index_list:
                    entity.append(record[index])
                self._entity_dict[key] = entity
        db_helper.close()

    def build_dict_by_db(self, sql, db_helper, key_index_list, entity_index_list):
        """
        根据输入键-值索引序列，对应sql语句中读取字段的的索引号建立字典
        key：
        若key_index_list长度为1，则直接以record[key_index_list[0]]为key
        若key_index_list长度大于1，则key为一个元组
        value：
        若entity_index_list长度为1，record[entity_index_list[0]]为value
        若entity_index_list长度大于1，value为一个list
        @param sql: sql语句
        @param db_helper: 数据库
        @param key_index_list: 键 索引序列
        @param entity_index_list:值 索引序列
        """
        record_list = db_helper.read(sql)
        for record in record_list:
            key_entity = []
            if len(key_index_list) == 1:
                key = record[key_index_list[0]]
                if type(key) == unicode:
                    key = key.encode("utf8")
            else:
                for index in key_index_list:
                    key_entity.append(record[index])
                key = tuple(key_entity)
            entity = []
            if len(entity_index_list) == 1:
                self._entity_dict[key] = record[entity_index_list[0]]
            else:
                for index in entity_index_list:
                    entity.append(record[index])
                self._entity_dict[key] = entity

    def add(self, key, value):
        if key in self._entity_dict:
            return
        self._entity_dict[key] = value

    def query(self, key):
        if key in self._entity_dict:
            return self._entity_dict[key]


if __name__ == "__main__":
    pass
