#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: PluginBase.py
# @time: 2021/2/18 20:27

from abc import ABCMeta, abstractmethod


class PluginBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def beforeRun(self):
        """
        运行前执行逻辑
        :return:
        """
        pass

    @abstractmethod
    def afterRun(self):
        """
        运行后执行逻辑
        :return:
        """
        pass
