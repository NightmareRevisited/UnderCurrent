#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Graph.py
# @time: 2021/2/20 15:58
from internal.base.AnubisRoot import AnubisRoot
from collections import defaultdict


class Graph(AnubisRoot):
    '''
    工作流节点有向图
    '''

    def __init__(self):
        self.inDegree = defaultdict(int)  # 入度字典，存放每个节点的入度
        self.outDegree = defaultdict(list)  # 出度字典，存放每个节点指向的
        self.graph = []  # 边列表

    def addEdge(self, start, end):
        '''
        添加有向边
        :param start: 起始点
        :param end: 终止点
        :return:
        '''
        self.inDegree[end] += 1
        self.inDegree[start] = self.inDegree[start]
        self.outDegree[start].append(end)
        self.graph.append([start, end])

    def hasCircle(self):
        '''
        检查有向图中是否有环
        :return:
        '''

        ## 拓扑排序
        while True:
            isBreak = True
            for point in self.inDegree.keys():
                if self.inDegree[point] == 0:
                    isBreak = False
                    self.inDegree.pop(point)
                    if point in self.outDegree:
                        for eP in self.outDegree.pop(point):
                            self.inDegree[eP] -= 1
            if isBreak:
                break
        if len(self.inDegree) == 0:
            return False, []
        else:
            return True, self.inDegree.keys()
