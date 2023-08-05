#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2020/10/21 17:15
@Author  : zhouj
@Email   : zhoujin9611@163.com
@phone   : 13937158462
@Software: PyCharm
"""

from setuptools import setup, find_packages

setup(
    name="test_pro",
    version="1.0.0",
    description="Quantitative trading ",
    author="zhoujin",
    url="https://upload.pypi.org/legacy/",
    author_email="zhoujin9611@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

# python setup.py sdist bdist_wininst upload -r http://example.com/pypi
# python setup.py sdist bdist_wininst upload -r https://upload.pypi.org/legacy/
# python setup.py sdist upload -r https://upload.pypi.org/legacy/
