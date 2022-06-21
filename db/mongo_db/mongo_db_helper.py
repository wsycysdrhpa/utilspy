#!/usr/bin/python
# -*- coding: utf8 -*-

# @version: 1.0
# @author: luojie
# @date: '15-10-14'


import pymongo


class MongoDbHelper():
    def __init__(self, host, db, port=27017, auth=False):
        self._conn = None
        self._client = None
        self._database = None
        self._image_files = None
        if auth:
            self.open_with_auth(host, db)
        else:
            self.open(host, db,  port)
        pass

    def open(self, host, db, port=27017):
        self._client = pymongo.MongoClient(host, port)
        self._database = self._client[db]

    def open_with_auth(self, host, db):
        self._client = pymongo.MongoClient(host)
        self._database = self._client[db]

    def create_collection(self, collection_name):
        self._database.create_collection(collection_name)

    def get_database(self):
        return self._database

    def get_collection(self, collection_name):
        return self._database[collection_name]

    # def find_one(self, collection_name, condition=None):
    #     # return_type: {}
    #     return self._database[collection_name].find_one(condition)
    #
    # def find(self, collection_name, condition=None):
    #     # return_type: Cursor, 迭代器
    #     return self._database[collection_name].find(condition)
    #
    # def insert(self, collection_name, items):
    #     list = self._database[collection_name]
    #     return list.insert(items)
    #
    # def clear(self, collection_name):
    #     self._database[collection_name].remove()

    def close(self):
        self._client.close()


if __name__ == "__main__":
    pass
    from utilspy.db.mongo_db.mongo_dao import MongoDao
    mongo_db_helper = MongoDbHelper("mongodb://luojie:kaimen@127.0.0.1:27017/admin", "heweather")
    mongo_dao = MongoDao("aqi_station", mongo_db_helper)
    print mongo_dao.find_one()
