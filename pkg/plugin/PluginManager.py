#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: PluginManager.py
# @time: 2021/1/12 20:23

import importlib


# class DispPluginManager(object):
#     @classmethod
#     def registPlugin(cls, func, pluginName, kwargs):
#         """
#         注册插件
#         :param function func: 插件运行函数
#         :param str pluginName:  插件名
#         :param dict kwargs:  插件列表
#         :return:
#         """
#         pluginFunc = cls.getPlugin(pluginName)
#
#         def wrapper():
#             pluginFunc(func, kwargs)
#
#         return wrapper
#
#     @classmethod
#     def getPlugin(cls, pluginName):
#         try:
#             pluginFunc = getattr(Plugin, pluginName)
#         except AttributeError:
#             raise AttributeError("Plugin function [ %s ] does not exist!" % pluginName)
#
#         return pluginFunc


class PluginManager(object):
    def __init__(self):
        self.pluginList = []

    def registPlugin(self, pluginName, kwargs):
        try:
            module = importlib.import_module("Plugin")
            pluginCls = getattr(module,pluginName)

        except AttributeError:
            raise AttributeError("Plugin [ %s ] does not exist!" % pluginName)

        self.pluginList.append(pluginCls(kwargs))

    def beforeRun(self):
        for i in range(len(self.pluginList)):
            self.pluginList[i].beforeRun()

    def afterRun(self):
        for i in range(len(self.pluginList) - 1, -1, -1):
            self.pluginList[i].afterRun()


