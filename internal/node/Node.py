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
        'selfSemaphore',
        'sonSemaphore',
    ]

    def __init__(self, taskName, nodeInfo, param):
        self.taskName = taskName
        self.id = nodeInfo['id']
        self.desc = nodeInfo['desc']
        self.parent = nodeInfo.get("parent", [])
        self.selfSemaphore = Semaphore(max(0, 1 - len(self.parent)))
        self.plugins = nodeInfo.get('plugins', {})
        self.sonSemaphore = {}
        self.params = param
        NodePool().addNode(self)
        self.action = list(map(self.bindActionParam, nodeInfo['action']))
        for parentId in self.parent:
            parentNode = NodePool().getNode(parentId)
            if parentNode:
                parentNode.sonSemaphore[self.id] = self.selfSemaphore
            else:
                NodePool().registSonNode(parentId, self.id)
        self.registPlugin()

    def registSonSemaphore(self):
        sonList = NodePool().fetchSonNode(self.id)
        for s in sonList:
            sonNode = NodePool().getNode(s)
            self.sonSemaphore[sonNode.id] = sonNode.selfSemaphore

    def dealWithSonNode(self):
        for s in self.sonSemaphore:
            self.sonSemaphore[s].release()

    def run(self):
        for i in range(len(self.parent)):
            self.selfSemaphore.acquire()
        self.registSonSemaphore()
        if len(ErrorStack()) > 0:
            self.dealWithSonNode()
            return
        try:
            self.runAction()
        except Exception as e:
            raise e
        finally:
            self.dealWithSonNode()

    def registPlugin(self):
        for pName in self.plugins:
            PluginManager().registPlugin(self.run, pName, self.plugins[pName])

    def bindActionParam(self, action):
        '''
        注册参数
        :param str action:
        :return:
        '''
        comp = re.compile(Const.ACTION_PARAM_REGEX)
        findRes = comp.findall(action)
        for f in findRes:
            action = action.replace(f[0], self.params[f[1]])
        return action

    def runAction(self):
        startTime = time.ctime()
        startTimeStamp = time.time()
        for action in self.action:
            aStartTime = time.ctime()
            aStartTimeStamp = time.time()
            output, status = runCommand(action)
            Log().log('''
Run Command : %s
Command Status Code : %s
Command Output : %s
''' % (action, status, output))
            if status:
                Log().error(self.taskName, self.id, self.desc, startTime, time.ctime())
                raise ActionError(self.taskName, self.id, self.desc, action, status, output, aStartTime)
            else:
                Log().log(self.taskName, self.id, self.desc, action, aStartTime,
                          int(time.time() - aStartTimeStamp))
        Log().log(self.taskName, self.id, self.desc, startTime, time.time() - startTimeStamp)
