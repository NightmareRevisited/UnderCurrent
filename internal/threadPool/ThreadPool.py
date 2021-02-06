#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Pool.py
# @time: 2021/1/30 15:30

from pkg.classControl.Singleton import Singleton
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

class ThreadPool(Singleton):

    def __init__(self):


