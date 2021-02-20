#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Node.py
# @time: 2021/1/12 16:00

from threading import Semaphore
from internal.base.AnubisRoot import AnubisRoot
from internal.exception.AnubisError import ActionError
from NodePool import NodePool
from pkg.plugin.PluginManager import PluginManager
from pkg.log.Log import Log
from pkg.tools import runCommand
from internal.exception.ErrorStack import ErrorStack
import time
import re
import internal.consts as Const


class Node(AnubisRoot):
    __slots__ = [
        'id',
        'desc',
        'plugins',
        'parent',
        'action',
        'sonNodes',
    ]

    def __init__(self, root, nodeInfo):
        self.root = root
        self.taskName = root.taskName
        self.id = nodeInfo['id']
        self.desc = nodeInfo['desc']
        self.parent = nodeInfo.get("parent", [])
        self.sonNodes = {}
        self.params = root.params
        NodePool().addNode(self)
        self.action = list(map(self.bindActionParam, nodeInfo['action']))
        self.finishedAction = 0
        for parentId in self.parent:
            self.root.graph.addEdge(parentId, self.id)
            parentNode = NodePool().getNode(parentId)
            if parentNode:
                parentNode.sonNodes[self.id] = self
            else:
                NodePool().registSonNode(parentId, self.id)
        self.plugins = nodeInfo.get('plugins', [])
        self.registPlugin()
        if len(self.parent) == 0:
            self.root.rootNode.append(self)
        else:
            self.preposition = Semaphore(len(self.parent) - 1)

    def registSonNode(self):
        sonList = NodePool().fetchSonNode(self.id)
        for s in sonList:
            self.sonNodes[s] = NodePool().getNode(s)

    def dealWithSonNode(self):
        for s in self.sonNodes:
            self.root.prepareNode(self.sonNodes[s])

    def runNode(self):
        self.registSonNode()
        if len(ErrorStack()) > 0:
            self.dealWithSonNode()
            return
        try:
            self.run()
        except Exception as e:
            raise e
        finally:
            self.dealWithSonNode()

    def registPlugin(self):
        self.pluginManager = PluginManager()
        for pName, kwargs in self.plugins:
            self.pluginManager.registPlugin(pName, kwargs)

    def bindActionParam(self, action):
        '''
        注册参数
        :param str action:
        :return:
        '''
        comp = re.compile(Const.ACTION_PARAM_REGEX)
        findRes = comp.findall(action)
        for f in findRes:
            action = action.replace(f[0], str(self.params[f[1]]))
        return action

    def run(self):
        self.pluginManager.beforeRun()
        startTime = time.ctime()
        startTimeStamp = time.time()
        for action in self.action:
            aStartTime = time.ctime()
            output, status = runCommand(action)
            Log().log('''
=========================
Run Command : %s
Command Status Code : %s
Command Output : %s
=========================
''' % (action, status, output))
            if status:
                Log().error(self.taskName, self.id, self.desc, startTime, time.ctime())
                raise ActionError(self.taskName, self.id, self.desc, action, status, output, aStartTime)
            else:
                self.finishedAction += 1
        self.root.finishedNode += 1
        Log().log('''
*********************************************
NodeName:    %s
StartTime:  %s
CostTime:  %.2f
Action:  
%s
FinishedStatus: %d/%d
*********************************************
''' % (self.desc, startTime, time.time() - startTimeStamp, "\n".join(self.action), self.finishedAction,
       len(self.action)))
        self.pluginManager.afterRun()
