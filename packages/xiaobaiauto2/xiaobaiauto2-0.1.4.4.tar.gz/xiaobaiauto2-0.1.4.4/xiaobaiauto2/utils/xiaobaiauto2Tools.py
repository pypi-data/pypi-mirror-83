#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'xiaobaiauto2Tools.py'
__create_time__ = '2020/9/23 23:14'

import argparse, os, zipfile
from jmespath import search
from json import loads

def raw_headless(s: str = ''):
    # 数据分割处理（单个请求放在一起）
    s = s.strip()
    sLines = s.split('\n')
    _start_index = [i for i, _ in enumerate(sLines) if 'HTTP/' in _ or ':authority:' in _]
    _span_data = []
    for i, v in enumerate(_start_index):
        if v != _start_index[-1]:
            _span_data.append(sLines[v:_start_index[i+1]])
        else:
            _span_data.append(sLines[v:])


    # 数据分离(method、url、headers、data)
    result = []
    for request in _span_data:
        if 'HTTP/' in request[0]:
            _method = request[0].split(' ')[0]
            _headers = {}
            _headers_end = 0
            raw_header_data_list = request[1:]
            for _, j in enumerate(raw_header_data_list):
                _headers_end = _
                if '' == j:
                    break
                else:
                    _headers[j.split(': ')[0]] = j.split(': ')[1].strip()
            if raw_header_data_list.__len__() > _headers_end + 1:
                _data = ''.join([i for i in request[_headers_end + 1:] if i != ''])
            else:
                _data = ''
            _url = request[0].split(' ')[1]
            if '://' not in _url and '443' in _headers.get('Host'):
                _url = 'https://' + _headers.get('Host') + _url
            elif '://' not in _url and '443' not in _headers.get('Host'):
                _url = 'http://' + _headers.get('Host') + _url
            result.append(
                {
                    'method': _method,
                    'url': _url,
                    'headers': _headers,
                    'data': _data
                }
            )
        elif ':authority:' in request[0]:
            '''
            :authority: 域名
            :method:    方式
            :path:      地址
            :scheme:    协议
            '''
            _authority = request[0].split(':')[2].strip()
            _method = request[1].split(':')[2].strip()
            _path = request[2].split(':')[2].strip()
            _scheme = request[3].split(':')[2].strip()
            _url = _scheme + '://' + _authority + _path
            _headers = {}
            _headers_end = 0
            raw_header_data_list = request[4:]
            for _, j in enumerate(raw_header_data_list):
                _headers_end = _
                if '' == j:
                    break
                else:
                    _headers[j.split(': ')[0]] = j.split(': ')[1].strip()
            if raw_header_data_list.__len__() > _headers_end + 1:
                _data = ''.join([i for i in request[_headers_end + 1:] if i != ''])
            else:
                _data = ''
            result.append(
                {
                    'method': _method,
                    'url': _url,
                    'headers': _headers,
                    'data': _data
                }
            )
    return result

def har_headless(s: str = ''):
    search_result = search('log.entries[].request', loads(s))
    result = []
    for request in search_result:
        _method = request.get('method')
        _url = request.get('url')
        _headers = {}
        _data = ''
        for item in request.get('headers'):
            if item.get('name') not in [':method', ':path', ':authority', ':scheme']:
                _headers[item.get('name')] = item.get('value')
        if 'postData' in request.keys():
            if request.get('postData').get('mimeType') == 'application/json':
                _data = {}
                for item in request.get('postData').get('params'):
                    _data[item.get('name')] = item.get('value')
            else:
                for item in request.get('postData').get('params'):
                    _data += item.get('name') + '=' + item.get('value') + '&'
                _data = _data[:-1]
        result.append(
            {
                'method': _method,
                'url': _url,
                'headers': _headers,
                'data': _data
            }
        )
    return result

def raw_convert(raw: str = None, is_xiaobaiauto2: int = 0, is_har: bool = False) -> str:
    '''
    转换器
    :param raw:
    :param is_xiaobaiauto2:
    :param kwargs:
    :return:
    '''
    _code_top = '#! /usr/bin/env python\n'
    _code_pytest_import = 'from re import findall\n' \
                          'try:\n\timport pytest\n' \
                          '\timport requests\n' \
                          'except ImportError as e:\n' \
                          '\timport os\n' \
                          '\tos.popen("pip install pytest")' \
                          '\tos.popen("pip install requests")\n\n'
    _code_xiaobaiauto2_import = 'try:\n\timport pytest\n' \
                          '\tfrom xiaobaiauto2.xiaobaiauto2 import api_action, PUBLIC_VARS\n' \
                          'except ImportError as e:\n' \
                          '\timport os\n' \
                          '\tos.popen("pip install pytest")\n\n'
    _code_requests_import = 'from re import findall\n' \
                            'try:\n\timport requests\n' \
                            'except ImportError as e:\n' \
                            '\timport os\n' \
                            '\tos.popen("pip install requests")\n\n'
    _code_pytest_end = '\r# 脚本使用须知： ' \
                       '\r# pytest -s -v   运行当前目录所有test_*开头的脚本文件' \
                       '\r# pytest -s -v xxx.py 运行指定脚本文件' \
                       '\r# pytest -s -v --html=report.html  运行并将结果记录到HTML报告中' \
                       '\r# pytest其他运行方式参考https://pypi.org/project/xiaobaiauto2或官网说明'
    _code = ''
    if raw:
        if is_har:
            result = har_headless(raw)
        else:
            result = raw_headless(raw)
        for i, v in enumerate(result):
            if is_xiaobaiauto2 == 1:
                _code += f'''@pytest.mark.run(order={i+1})\
                \rdef test_xiaobai_api_{i+1}():\
                \r\t# 测试前数据准备\
                \r\theaders = {v.get('headers')}\
                \r\turl = '{v.get('url')}' \
                \r\tdata = '{v.get('data')}'\
                \r\tresponse = requests.request(method='{v.get('method')}', url=url, data=data, headers=headers, verify=False)\
                \r\t# 测试后时间判断/提取\
                \r\t# assert response.status_code == 200\
                \r\t# global var_name\
                \r\tif 'application/json' in response.headers['content-type']:\
                \r\t\t# assert '预期结果' == response.json()[路径]\
                \r\t\t# var_name = response.json()[路径]\
                \r\t\tprint(response.json())\
                \r\telse:\
                \r\t\t# assert '预期结果' in response.text\
                \r\t\t# var_name = findall('正则表达式', response.text)[0]\
                \r\t\tprint(response.text)\n\n'''
            elif is_xiaobaiauto2 == 2:
                _code += f'''@pytest.mark.run(order={i+1})\
                \rdef test_xiaobai_api_{i+1}():\
                \r\t# 测试前数据准备\
                \r\theaders = {v.get('headers')}\
                \r\turl = '{v.get('url')}' \
                \r\tdata = '{v.get('data')}'\
                \r\tapi_action(\
                \r\t\tmethod='{v.get('method')}', url=url, data=data, headers=headers, verify=False,\
                \r\t\tjson_path='', json_assert='', contains_assert='', _re='', _re_var='')\
                \r\t# 表达式中json_path与json_assert为判断json结果是否符合预期值\
                \r\t# 表达式中contains_assert为模糊判断返回值是否包含预期结果\
                \r\t# 表达式中_re与_re_var为提取数据为下游接口提供数据支持\n\n'''
            else:
                _code += f'''\r# 测试前数据准备\
                \rheaders = {v.get('headers')}\
                \rurl = '{v.get('url')}' \
                \rdata = '{v.get('data')}'\
                \rresponse = requests.request(method='{v.get('method')}', url=url, data=data, headers=headers, verify=False)\
                \r# 测试后数据判断/提取\
                \r# assert response.status_code == 200\
                \rif 'application/json' in response.headers['content-type']:\
                \r\t# assert '预期结果' == response.json()[路径]\
                \r\t# var_name = response.json()[路径]\
                \r\tprint(response.json())\
                \relse:\
                \r\t# assert '预期结果' in response.text\
                \r\t# var_name = findall('正则表达式', response.text)[0]\
                \r\tprint(response.text)\n\n'''
    if is_xiaobaiauto2 == 1:
        return _code_top + _code_pytest_import + _code + _code_pytest_end
    elif is_xiaobaiauto2 == 2:
        return _code_top + _code_xiaobaiauto2_import + _code + \
               '\n# 使用公共变量的格式：\n# PUBLIC_VARS["变量名"][0][0]  获取响应头中第一个匹配值' \
               '\n# PUBLIC_VARS["变量名"][1][0]  获取响应体中第一个匹配值' + _code_pytest_end
    else:
        return _code_top + _code_requests_import + _code

def api_raw():
    arg = argparse.ArgumentParser(
        '小白科技·Python代码转换器·raw版·浏览器·Fiddler·Charles'
    )
    arg.add_argument('-f', '--file', type=str, default='', help='支持txt|saz|har扩展名的raw数据文件')
    arg.add_argument('-d', '--dir',
                     type=str,
                     default='.',
                     help='批量转换指定目录下所有txt|saz|har扩展名的raw数据文件, 默认当前目录')
    arg.add_argument('-s', '--save', type=str, default='', help='默认生成同名的.py文件,省略.py扩展名')
    arg.add_argument('-x', '--xiaobai',
                     type=int,
                     choices=(0, 1, 2),
                     default=0,
                     help='0:requests格式(默认),1:pytest格式,2:xiaobaiauto2格式')
    params = arg.parse_args()
    if os.name == 'nt':
        step = '\\'
    else:
        step = '/'
    is_har = False
    if os.path.isfile(params.file):
        raw_data = ''
        if os.path.splitext(params.file)[1] == '.saz':
            is_har = False
            raw_file_path = os.path.splitext(params.file)[0]
            zipfile.ZipFile(params.file).extractall(raw_file_path)
            raw_file_list = [i for i in os.listdir(raw_file_path + step + 'raw') if '_c.txt' == i[-6:]]
            for i in raw_file_list:
                with open(raw_file_path + step + 'raw' + step + i, 'r') as fr:
                    raw_data += fr.read() + '\n\n\n'
                    fr.close()
            if os.path.isdir(raw_file_path):
                try:
                    os.remove(raw_file_path)
                except PermissionError as e:
                    pass
        elif os.path.splitext(params.file)[1] == '.har':
            is_har = True
            with open(params.file, 'r', encoding='utf-8') as fr:
                raw_data += fr.read()
                fr.close()
        elif os.path.splitext(params.file)[1] == '.har':
            with open(params.file, 'r', encoding='utf-8') as fr:
                is_har = False
                raw_data += fr.read()
                fr.close()
        code = raw_convert(raw=raw_data, is_xiaobaiauto2=params.xiaobai, is_har=is_har)
        if params.save:
            with open(params.save + '.py', 'w', encoding='utf-8') as fw:
                fw.write(code)
                fw.flush()
                fw.close()
        else:
            with open(os.path.splitext(params.file)[0] + '.py', 'w', encoding='utf-8') as fw:
                fw.write(code)
                fw.flush()
                fw.close()
    else:
        if params.file != '':
            if os.path.isfile(params.dir + step + params.file):
                raw_data = ''
                if os.path.splitext(params.dir + step + params.file)[1] == '.saz':
                    is_har = False
                    raw_file_path = os.path.splitext(params.dir + step + params.file)[0]
                    zipfile.ZipFile(params.dir + step + params.file).extractall(raw_file_path)
                    raw_file_list = [i for i in os.listdir(params.dir + step + raw_file_path + step + 'raw') if '_c.txt' == i[-6:]]
                    for i in raw_file_list:
                        with open(params.dir + step + raw_file_path + step + 'raw' + step + i, 'r') as fr:
                            raw_data += fr.read() + '\n\n\n'
                            fr.close()
                    if os.path.isdir(params.dir + step + raw_file_path):
                        try:
                            os.remove(params.dir + step + raw_file_path)
                        except PermissionError as e:
                            raise (e)
                elif os.path.splitext(params.dir + step + params.file)[1] == '.har':
                    is_har = True
                    with open(params.dir + '/' + params.file, 'r', encoding='utf-8') as fr:
                        raw_data += fr.read()
                        fr.close()
                elif os.path.splitext(params.dir + step + params.file)[1] == '.txt':
                    with open(params.dir + step + params.file, 'r', encoding='utf-8') as fr:
                        is_har = False
                        raw_data += fr.read()
                        fr.close()
                code = raw_convert(raw=raw_data, is_xiaobaiauto2=params.xiaobai, is_har=is_har)
                if params.save:
                    with open(params.dir + step + params.save + '.py', 'w', encoding='utf-8') as fw:
                        fw.write(code)
                        fw.flush()
                        fw.close()
                else:
                    with open(os.path.splitext(params.dir + step + params.file)[0] + '.py', 'w', encoding='utf-8') as fw:
                        fw.write(code)
                        fw.flush()
                        fw.close()
        else:
            for f in [i for i in os.listdir(params.dir) if os.path.splitext(i)[1] in ['.saz', '.har', '.txt']]:
                raw_data = ''
                if os.path.splitext(params.dir + step + f)[1] == '.saz':
                    is_har = False
                    raw_file_path = os.path.splitext(params.dir + step + f)[0]
                    zipfile.ZipFile(params.dir + step + f).extractall(raw_file_path)
                    raw_file_list = [i for i in os.listdir(raw_file_path + step + 'raw') if
                                     '_c.txt' == i[-6:]]
                    for i in raw_file_list:
                        with open(raw_file_path + step + 'raw' + step + i, 'r') as fr:
                            raw_data += fr.read() + '\n\n\n'
                            fr.close()
                    if os.path.isdir(raw_file_path):
                        try:
                            os.remove(raw_file_path)
                        except PermissionError as e:
                            pass
                elif os.path.splitext(params.dir + step + f)[1] == '.har':
                    is_har = True
                    with open(params.dir + step + f, 'r', encoding='utf-8') as fr:
                        raw_data += fr.read()
                        fr.close()
                elif os.path.splitext(params.dir + step + f)[1] == '.txt':
                    with open(params.dir + step + f, 'r', encoding='utf-8') as fr:
                        is_har = False
                        raw_data += fr.read()
                        fr.close()
                code = raw_convert(raw=raw_data, is_xiaobaiauto2=params.xiaobai, is_har=is_har)
                if params.save:
                    with open(params.dir + step + params.save + '.py', 'w', encoding='utf-8') as fw:
                        fw.write(code)
                        fw.flush()
                        fw.close()
                else:
                    with open(os.path.splitext(params.dir + step + f)[0] + '.py', 'w', encoding='utf-8') as fw:
                        fw.write(code)
                        fw.flush()
                        fw.close()