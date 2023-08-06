# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""
import json


class RedisHandler:
    def __init__(self, redis_instance, key_prefix, custom_func):
        self.redis_instance = redis_instance
        self.key_prefix = key_prefix
        self.custom_func = custom_func

    def insert_data(self, serialized_data):
        if self.custom_func:
            serialized_data = self.custom_func(serialized_data)
        else:
            serialized_data = json.loads(serialized_data)
        key = f'{self.key_prefix}:{serialized_data["record"]["time"]["timestamp"]}'
        self.redis_instance.set(key, json.dumps(serialized_data))
