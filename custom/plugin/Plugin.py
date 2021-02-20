#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Plugin.py
# @time: 2021/2/20 15:37

from __future__ import print_function
from pkg.plugin.PluginBase import PluginBase
from pkg.log.Log import Log

def print(*args):
    Log().log(*args)


class Test(PluginBase):
    def __init__(self, test1, test2):
        self.test1 = test1
        self.test2 = test2

    def beforeRun(self):
        print("This is a test plugin")

    def afterRun(self):
        print("This is a test plugin")
