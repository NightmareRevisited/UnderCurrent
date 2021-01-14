#!/usr/bin/env python
#-*- coding:utf-8 -*-

# @author: NightmareRevisited
# @project: UnderCurrent
# @file: setup
# @time: 2019/5/9 14:32
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
        name='anubis',
        version='1.0',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'threadpool',
        ],
        entry_points='''
        [console_scripts]
        undercurrent=undercurrent.cli:main
    ''',
)
