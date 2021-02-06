#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: ThreadPool.py
# @time: 2021/1/13 10:39

from pkg.consts import THREAD_POOL_SIZE
from Worker import Worker
from threading import Lock
try:
    from queue import Queue
except:
    from Queue import Queue


class ThreadPool(object):
    def __init__(self, size=-1):
        self.errorStack = []
        if size > 0:
            poolSize = size
        else:
            poolSize = THREAD_POOL_SIZE
        self.freeThreadNum = poolSize
        self.lock = Lock()
        self.workerList = []
        self.taskQueue = Queue()
        self.isRunning = True
        for i in range(poolSize):
            workerThread = Worker(self)
            self.workerList.append(workerThread)
            workerThread.start()

    def updateFreeThreadNum(self,updateNum):
        with self.lock:
            self.freeThreadNum += updateNum

    def submit(self, func, args):
        '''
        :param func: function
        :param args: list
        :return:
        '''
        self.taskQueue.put((func, args))

    def getTask(self, block=True, timeout=None):
        return self.taskQueue.get(block, timeout)
