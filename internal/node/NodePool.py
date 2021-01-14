#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: NodePool.py
# @time: 2021/1/12 16:02

from pkg.classControl.Singleton import Singleton
from collections import defaultdict


class NodePool(Singleton):
    def __init__(self):
        self.pool = dict()
        self.sonNode = defaultdict(list)

    def addNode(self, node):
        self.pool[node.id] = node

    def getNode(self, id):
        return self.pool.get(id, None)

    def registSonNode(self, id, sonId):
        self.sonNode[id].append(sonId)

    def fetchSonNode(self, id):
        return self.sonNode[id]
