#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Singleton.py
# @time: 2021/1/12 18:19

class SingletonMeta(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(SingletonMeta,self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(SingletonMeta,self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Singleton(object):
    __metaclass__ = SingletonMeta