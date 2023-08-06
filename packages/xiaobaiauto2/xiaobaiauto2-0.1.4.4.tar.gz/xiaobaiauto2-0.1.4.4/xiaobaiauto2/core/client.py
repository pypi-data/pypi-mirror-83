#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'client.py'
__create_time__ = '2020/9/18 13:50'

from typing import DefaultDict
from requests import request, RequestException
from jmespath import search
from re import findall
import pysnooper

env = {}

class Request(object):
    def __init__(self, title=''):
        self.title = title

    def __call__(self, func):
        def wrapper(**kwargs):
            test = {}
            env_data = {}
            global env
            if 'before' in kwargs.keys():
                for params, value in kwargs.items():
                    if params in ['before', 'after']:
                        continue
                    else:
                        k_list = findall('\{(.+?)\}', str(value))
                        if k_list.sort() == list(dict(kwargs['before']).keys()).sort():
                            kwargs[params] = str(value).format_map(kwargs['before'])
                        else:
                            for k in k_list:
                                if k in dict(kwargs['before']).keys():
                                    kwargs[params] = str(value).replace('{' + k +'}', kwargs['before'][k])
                kwargs.pop('before')
            if 'after' in kwargs.keys():
                if 'test' in dict(kwargs['after']).keys():
                    test = kwargs['after']['test']
                if 'env' in dict(kwargs['after']).keys():
                    env_data = kwargs['after']['env']
                kwargs.pop('after')
            '''
            {
                'before': {
                    'a': 1, 
                    'b': 2
                },
                'after': {
                    'test': {
                        'json': [{'with':'body', 'path': 'code', 'value': 'xiaobai'}], 
                        'match': [{'with':'body', 'path': 0, 'value': 'xiaobai'}]
                    },
                    'env': {
                        'json': [{'with':'body', 'path': 'code', 'name': 'xiaobai'}], 
                        'match': [{'with':'body', 'path': 'ni(.+?)hao', 'name': 'xiaobai'}]
                    }
                }
            }
            with的值：body,headers,status
            '''
            try:
                res = request(**kwargs)
                if test != {}:
                    if 'json' in test.keys():
                        for j in test['json']:
                            j = dict(j)
                            if j.get('with') == 'body':
                                assert j.get('value') == search(j.get('path'), res.json())
                            elif j.get('with') == 'headers':
                                assert j.get('value') == search(j.get('path'), res.headers)
                            elif j.get('with') == 'status':
                                raise ('状态码不能使用json格式')
                    elif 'match' in test.keys():
                        for m in test['json']:
                            m = dict(m)
                            if m.get('with') == 'body':
                                assert m.get('value') in res.text
                            elif m.get('with') == 'headers':
                                assert m.get('value') in res.headers.__str__()
                            elif m.get('with') == 'status':
                                assert m.get('value') in res.status_code
                    else:
                        exit(-1)
                        raise ('参数有误')
                if env_data != {}:
                    if 'json' in test.keys():
                        for j in test['json']:
                            j = dict(j)
                            if j.get('with') == 'body':
                                env[j.get('name')] = search(j.get('path'), res.json())
                            elif j.get('with') == 'headers':
                                env[j.get('name')] = search(j.get('path'), res.headers)
                            elif j.get('with') == 'status':
                                env[j.get('name')] = res.status_code
                    elif 'match' in test.keys():
                        for m in test['json']:
                            m = dict(m)
                            if m.get('with') == 'body':
                                env[m.get('name')] = findall(m.get('path'), res.text)
                            elif m.get('with') == 'headers':
                                env[m.get('name')] = findall(m.get('path'), res.headers.__str__())
                            elif m.get('with') == 'status':
                                env[m.get('name')] = res.status_code
                    else:
                        exit(-1)
                        raise ('参数有误')
            except RequestException as e:
                exit(-1)
                raise ('请求参数有误', e)
            print(self.title, '执行完测试')
            return func()
        return wrapper