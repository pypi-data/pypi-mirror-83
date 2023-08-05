#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2020/10/15 17:52
@Author  : zhouj
@Email   : zhoujin9611@163.com
@phone   : 13937158462
@Software: PyCharm
"""
from setuptools import setup, find_packages

setup(
    name="AiPangu",
    version="1.0.0",
    description="Quantitative trading ",
    author="zhoujin",
    url="https://upload.pypi.org/legacy/",
    author_email="zhoujin9611@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy", "pandas", "matplotlib", "tushare", "requests"]
)
