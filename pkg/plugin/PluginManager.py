#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: PluginManager.py
# @time: 2021/1/12 20:23

from pkg.classControl.Singleton import Singleton
from collections import defaultdict

class PluginManager(Singleton):
    def __init__(self):
        self.pluginMap = defaultdict(list)

    def registPlugin(self, func, pluginName, args):
        pass
