#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lxch
#############################################


from setuptools import setup, find_packages

setup(
    name = "requestQ",
    version = "0.0.6",
    keywords = ["pip", "request","requests", "requestQ"],
    description = "封装了requests去接口测试",
    long_description = "本次更新修改源码的url",
    license = "MIT Licence",

    url = "https://gitee.com/tuboyou/requestQ",
    author = "lxch",
    author_email = "lixuechengde@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['PyMySQL','requests']
)