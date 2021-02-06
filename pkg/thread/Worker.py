#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Worker.py
# @time: 2021/2/6 9:28
from threading import currentThread, Thread


class Worker(Thread):
    def __init__(self, threadPool):
        """
        :param ThreadPool threadPool: 线程池
        """
        Thread.__init__(self)
        self.pool = threadPool
        self.waitStatus = True
        self.daemon = True

    def run(self):
        while True:
            func, args = self.pool.getTask()
            self.waitStatus = False
            self.pool.updateFreeThreadNum(-1)
            func(*args)
            self.waitStatus = True
            self.pool.updateFreeThreadNum(1)
