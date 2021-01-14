#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: ErrorStack.py
# @time: 2021/1/13 18:07

from pkg.classControl.Singleton import Singleton
from pkg.log.Log import Log


class ErrorStack(Singleton):
    def __init__(self):
        self.stack = []

    def add(self, error):
        self.stack.append(error)

    def logError(self):
        while len(self.stack) > 0:
            err = self.stack.pop()
            Log().error(err.message)

    def __len__(self):
        return len(self.stack)
