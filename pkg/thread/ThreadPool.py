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
        """
        初始化线程池
        :param int size: 线程池大小，为负将会设置为默认大小
        """
        self.errorStack = []
        if size > 0:
            poolSize = size
        else:
            poolSize = THREAD_POOL_SIZE
        self.freeThreadNum = poolSize
        self.lock = Lock()
        self.workerList = []
        self.taskQueue = Queue()
        for i in range(poolSize):
            workerThread = Worker(self)
            self.workerList.append(workerThread)
            workerThread.start()

    def updateFreeThreadNum(self,updateNum):
        """
        更新闲置线程数
        :param int updateNum:
        :return:
        """
        with self.lock:
            self.freeThreadNum += updateNum

    def submit(self, func, args):
        '''
        向线程池中提交任务
        :param func func: 任务函数
        :param list args: 任务参数
        :return:
        '''
        self.taskQueue.put((func, args))

    def getTask(self, block=True, timeout=None):
        """
        从任务队列中取一个任务
        :param bool block: 是否阻塞
        :param None|int timeout: 超时时间
        :return:
        """
        return self.taskQueue.get(block, timeout)
