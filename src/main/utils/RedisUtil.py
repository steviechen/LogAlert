# coding=utf-8
import redis
import json
from src.main.utils import ConfigurationUtil

class RedisUtil(object):
    config_key = 'redis'

    def __init__(self):
        self.host = ConfigurationUtil.get(self.config_key, 'host')
        self.port = ConfigurationUtil.get(self.config_key, 'port')
        self.db = ConfigurationUtil.get(self.config_key, 'db')
        self.password = ConfigurationUtil.get(self.config_key, 'password')
        self.redis_pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password = self.password)
        self.redis_client = redis.Redis(connection_pool=self.redis_pool)
        # self.redis_client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def clear_all(self):
        self.redis_client.flushdb()

    def delete_key(self, keystr):
        key_list = []
        for key in self.redis_client.scan_iter(match=keystr + '*', count=10000):
            key_list.append(key)

        for key in key_list:
            self.redis_client.delete(key)

    def get_All_Keys(self):
        return self.redis_client.keys('*')

    def keyExists(self, key):
        return self.redis_client.exists(key)

    def set_single_data(self, key, value, expire=3600 * 24 * 30):
        self.redis_client.setex(key, expire, value)

    def get_single_data(self,key):
        return self.redis_client.get(key)

    def set_cache_data(self, contents=None, expire=3600 * 24 * 30):
        if contents is None:
            contents = {}
        for k, v in contents.items():
            self.redis_client.setex(k, expire, json.dumps(v))

    def get_cache_data(self, key):
        keys = self.redis_client.keys(key + "*")
        pipe = self.redis_client.pipeline()
        pipe.mget(keys)
        res_ls = []
        for (k, v) in zip(keys, pipe.execute()):
            nv = list(filter(lambda item: True if item is not None else False, v))
            res_ls.extend([json.loads(item) for item in nv])
        return res_ls

    def get_cache_bluk_data(self, keys):
        pipe = self.redis_client.pipeline()
        pipe.mget(keys)
        res_ls = []
        for (k, v) in zip(keys, pipe.execute()):
            nv = list(filter(lambda item: True if item is not None else False, v))
            res_ls.extend([json.loads(item) for item in nv])
        return res_ls



