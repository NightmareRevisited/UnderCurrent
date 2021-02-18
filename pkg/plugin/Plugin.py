#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Plugin.py
# @time: 2021/1/13 11:09

from __future__ import print_function
import time
from PluginBase import PluginBase

try:
    from inspect import signature
except:
    from funcsigs import signature


# 非debug模式禁用builtin-print函数，会导致输出错乱
# DEBUG模式把下行注释掉
# print = Log().log


# class Plugin(object):
#     __metaclass__ = PluginMeta
#     '''
#     插件类
#
#     新增插件必须为ClassMethod
#     参数有且只能有func和kwarg
#     '''
#
#     @classmethod
#     def testPlugin(cls, func, kwargs):
#         """
#         :param callable func: 需要插件的函数
#         :param dict kwargs: 参数字典
#         :return:
#         """
#         print("This is a test plugin!")
#         func()
#         print("Test finished~")
#
#     @classmethod
#     def testPlugin1(cls, func, kwargs):
#         """
#         :param callable func: 需要插件的函数
#         :param dict kwargs: 参数字典
#         :return:
#         """
#         print("This is a test plugin!")
#         func()
#         print("Test finished~")


class TimePlugin(PluginBase):
    def beforeRun(self):
        self.startTime = time.time()

    def afterRun(self):
        print(time.time() - self.startTime)
