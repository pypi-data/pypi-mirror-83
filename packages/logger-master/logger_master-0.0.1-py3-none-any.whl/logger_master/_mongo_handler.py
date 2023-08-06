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


class MongoHandler:
    def __init__(self, mongo_instance, database, collection, custom_func):
        self.mongo_instance = mongo_instance
        self.database = database
        self.collection = collection
        self.custom_func = custom_func

    def insert_data(self, serialized_data):
        if self.custom_func:
            serialized_data = self.custom_func(serialized_data)
        else:
            serialized_data = json.loads(serialized_data)
        self.mongo_instance[self.database][self.collection].insert_one(serialized_data)

