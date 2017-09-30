# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '15-5-28'


import redis


class RedisClient(object):
    def __init__(self, host, port=6379, db=0):
        self._pool = redis.ConnectionPool(host=host, port=port, max_connections=100, db=db)
        #self._redis = redis.Redis(host, port)

    def set(self, key, value, expire=None):
        r = redis.Redis(connection_pool=self._pool)
        r.set(key, value)
        if expire:
            r.expire(key, expire)

    def set_batch(self, item_list):
        r = redis.Redis(connection_pool=self._pool)
        pipe = r.pipeline()
        for key, value, expire in item_list:
            pipe.set(key, value)
            if expire:
                pipe.expire(key, expire)
        pipe.execute()

    def get_batch(self, key_list):
        data_map = {}
        r = redis.Redis(connection_pool=self._pool)
        for key in key_list:
            data_map[key] = r.get(key)
        return data_map

    def get(self, key):
        r = redis.Redis(connection_pool=self._pool)
        return r.get(key)

    def rpush(self, key, value, expire=None):
        # 向值list右边添加value（可以是元组,list）
        r = redis.Redis(connection_pool=self._pool)
        if isinstance(value, (list, tuple)):
            r.rpush(key, *value)
        else:
            r.rpush(key, value)
        if expire:
            r.expire(key, expire)
        pass

    def expire(self, key, expire):
        if expire:
            r = redis.Redis(connection_pool=self._pool)
            r.expire(key, expire)

    def ttl(self, key):
        r = redis.Redis(connection_pool=self._pool)
        return r.ttl(key)

    def get_list(self, key, start=0, end=-1):
        r = redis.Redis(connection_pool=self._pool)
        return r.lrange(key, start, end)

    def rename(self, key, new_key):
        r = redis.Redis(connection_pool=self._pool)
        r.rename(key, new_key)
        pass

    def delete(self, key):
        r = redis.Redis(connection_pool=self._pool)
        return r.delete(key)

    def close(self):
        self._pool.disconnect()


if __name__ == "__main__":
    rc = RedisClient("10.10.10.124")
    print rc.get_list("DCS_dcs_qt_channel_ondemands_125090_bak", 0, -1)
    pass
