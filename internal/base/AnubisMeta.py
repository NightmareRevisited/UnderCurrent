#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: AnubisMeta.py
# @time: 2021/1/12 18:09
import logging

try:
    from inspect import signature
except:
    from funcsigs import signature


class AnubisMetaClass(type):
    # def __new__(cls, clsname, bases, clsdict):
    #     for name in clsdict:
    #         if name.lower() != name:
    #             raise TypeError('Bad attribute name: ' + name)
    #     return super(AnubisMetaClass, cls).__new__(cls, clsname, bases, clsdict)

    def __init__(self, clsname, bases, clsdict):
        super(AnubisMetaClass, self).__init__(clsname, bases, clsdict)
        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            prev_dfn = getattr(sup, name, None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning('Signature mismatch in %s. %s != %s',
                                    ".".join([value.__class__.__name__, value.__name__]), prev_sig, val_sig)
