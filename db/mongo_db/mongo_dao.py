# -*- coding:utf-8 -*-

# @version: 1.0
# @author: luojie
# @date: '2015/10/29'


import json

from pymongo.collection import Collection

from utilspy.entity.entity_buffer import EntityBuffer
from utilspy.file.file_helper import FileHelper


class MongoDao(Collection):
    def __init__(self, collection_name, mongo_db_helper):
        Collection.__init__(self, mongo_db_helper.get_database(), collection_name)
        pass


if __name__ == "__main__":
    pass
    from utilspy.db.mongo_db.mongo_db_helper import MongoDbHelper
    mongo_db_helper = MongoDbHelper("10.10.10.123", "music")
    dao = MongoDao("musicInfo", mongo_db_helper)
    data_files = FileHelper.get_file_list("E:/work/yzs/dcs/data/xiami/musicInfo")
    entity_buffer = EntityBuffer(1000)
    for data_file_path in data_files:
        with open(data_file_path, "r") as data_file:
            for line in data_file:
                music_info = json.loads(line)
                if not music_info["song_id"]:
                    continue
                entity_buffer.add_entity(music_info)
                if entity_buffer.is_full():
                    dao.insert_many(entity_buffer.get_all_entities())
                    entity_buffer.empty()
    if entity_buffer.get_all_entities():
        dao.insert_many(entity_buffer.get_all_entities())
        entity_buffer.empty()
    mongo_db_helper.close()
