#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: AnubisError.py
# @time: 2021/1/12 14:32


class AnubisError(StandardError):
    pass


class NodeError(AnubisError):
    pass


class ActionError(AnubisError):
    def __init__(self, taskName, nodeId, nodeDesc, action, status, output, occurTime):
        self.message = '''
taskName: %s
nodeId: %s
nodeDesc: %s
action: %s
statusCode: %s
output: %s,
occurTime: %s,
        ''' % (taskName, nodeId, nodeDesc, action, status, output, occurTime)
