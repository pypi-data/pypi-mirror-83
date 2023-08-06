#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = '__init__.py'
__create_time__ = '2020/10/4 21:49'

from xiaobaiauto2.core.client import Request

@Request(title='测试登录接口')
def test_login():
    pass