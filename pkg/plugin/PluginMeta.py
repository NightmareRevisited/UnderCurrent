#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: PluginMeta.py
# @time: 2021/2/18 19:46

from new import instancemethod
from functools import wraps

class PluginMeta(type):
    """
    声明插件中只允许定义classmethod
    且动态绑定输入参数检查

    该类代码如果看不明白，查阅https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p09_meta_programming.html
    没搞懂每个变量和函数含义前，禁止修改此类
    """

    def __init__(self, clsname, bases, clsdict):
        super(PluginMeta, self).__init__(clsname, bases, clsdict)

        for name in clsdict:
            if name.startswith('_'):
                continue

            clsmethod = clsdict[name]
            if callable(clsmethod):
                raise AttributeError("Plugin function [ %s ]  must be classmethod or staticmethod!" % name)
            valueFunction = clsmethod.__func__

            if valueFunction.__code__.co_argcount != 3:
                raise AttributeError("Plugin function [ %s ] arguments error: ",
                                     "".join(valueFunction.__code__.co_varnames))

            @wraps(valueFunction)
            def wrapper(cls, func, kwargs):
                if not callable(func):
                    raise TypeError("Plugin function [ %s ] argument [ func ] must be callable object!" % name)

                if not isinstance(kwargs, dict):
                    raise TypeError("Plugin function [ %s ] argument [ kwargs ] must be dict")

                valueFunction(cls, func, kwargs)

            setattr(self, name, instancemethod(wrapper, self))
