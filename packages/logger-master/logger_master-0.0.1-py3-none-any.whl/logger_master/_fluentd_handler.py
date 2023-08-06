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
from fluent import sender


class FluentdHandler:
    def __init__(self, hostname, port, key_prefix, custom_func):
        self.logger = sender.FluentSender(key_prefix, host=hostname, port=port)
        self.key_prefix = key_prefix
        self.custom_func = custom_func

    def insert_data(self, serialized_data):
        if self.custom_func:
            serialized_data = self.custom_func(serialized_data)
        else:
            serialized_data = json.loads(serialized_data)
        self.logger.emit('follow', serialized_data)
