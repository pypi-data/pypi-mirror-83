#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'test_case1.py'
__create_time__ = '2020/10/4 21:44'

from xiaobaiauto2.test.APIs import test_login
import pytest



test_login(method='POST',
        url='{host}{path}',
        before={'path': '/', 'host': 'http://127.0.0.1:8000'},
        after={'test': {'json': [{'with': 'body', 'path': 'detail', 'value': 'Not Found0000'}]}})

