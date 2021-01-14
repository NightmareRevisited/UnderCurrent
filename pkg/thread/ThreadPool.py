#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: ThreadPool.py
# @time: 2021/1/13 10:39

import threadpool
from pkg.classControl.Singleton import Singleton


class ThreadPool(Singleton):
    def __init__(self, size):
        self.threadPool = threadpool.ThreadPool(size)
        self.errorStack = []

    def submit(self, func, args):
        '''
        :param func: function
        :param args: list
        :return:
        '''
