import random
import json
from collections import OrderedDict

valid_requests = ['POST', 'GET']

def parse_line(line):
    """
    {'status_code': '200', 'date': '08/Jan/2018', 'interface': 'ubas010001', 'method': 'POST'}
    """
    splits = line.split(' ')
    method = splits[5].replace('"','')
    if method not in valid_requests:
        return False
    datetime = splits[3].split(':')
    date = datetime[0].replace('[','')
    hour = datetime[1]
    minute = datetime[2]
    seconds = datetime[3]
    interface = splits[6].split('/')[2]
    return dict(method=method, date=date, status_code=splits[8],
                interface=interface)

def count_by_interface(file):
    response = OrderedDict()
    total = 0
    with open(file, 'r', encoding='utf8') as fh:
        for line in fh:
            line = line.replace('\n', '')
            result = parse_line(line)
            if not result:
                continue
            date = result.get('date')
            interface = result.get('interface')
            if date not in response.keys():
                response[date] = {}
            if interface not in response[date].keys():
                response[date][interface] = 1
            else:
                response[date][interface] = response[date][interface] + 1

    return response

def count_by_day(file):
    response = OrderedDict()
    total = 0
    with open(file, 'r', encoding='utf8') as fh:
        for line in fh:
            line = line.replace('\n', '')
            result = parse_line(line)
            if not result:
                continue
            total += 1
            date = result.get('date')
            method = result.get('method')
            status_code = result.get('status_code')
            if date not in response.keys():
                response[date] = {}
                response[date]['count'] = 1
            else:
                response[date]['count'] = response[date]['count']+1
            if status_code not in response[date].keys():
                response[date][status_code] = 1
            else:
                response[date][status_code] = response[date][status_code]+1
            if method not in response[date].keys():
                response[date][method] = 1
            else:
                response[date][method] = response[date][method]+1
    response['total'] = total
    return response

def count_by_min(file):
    # 根据分钟数统计
    result = OrderedDict()
    total = 0
    with open(file, 'r', encoding='utf8') as fh:
        for line in fh:
            line = line.replace('\n', '')
            splits = line.split(' ')
            method = splits[5].replace('"','')
            if method not in valid_requests:
                continue
            total += 1
            datetime = splits[3].split(':')
            date = datetime[0].replace('[','')
            hour = datetime[1]
            minute = datetime[2]
            seconds = datetime[3]
            if date not in result.keys():
                result[date] = {}
            if hour not in result.get(date).keys():
                result[date][hour] = {}
            if minute not in result.get(date).get(hour).keys():
                result[date][hour][minute] = 1
            else:
                result[date][hour][minute] = result[date][hour][minute] + 1

    response = {}
    for key, value in result.items():
        if key not in response.keys():
            response[key] = {}
            response[key]['counts'] = []
        for v in value.values():
            for i in v.values():
                response[key]['counts'].append(i)

    r = {}
    for key, value in response.items():
        for v in value.values():
            v.sort(reverse=True)
            r[key] = v[0:5]
    return r

def main():
    print('===========日志统计V2.2=============')
    print('=========Update: 新增接口统计=========')
    print('========只统计请求方法是GET和POST的=======')
    while True:
        op = input('请选择 1.按天统计 2.按分钟统计 3.按接口统计')
        path = input('请输入文件路径：')
        if op == '2':
            try:
                result = count_by_min(path)
            except Exception as e:
                print(e)
                continue
        elif op == '1':
            try:
                result = count_by_day(path)
            except Exception as e:
                print(e)
                continue
        elif op == '3':
            try:
                result = count_by_interface(path)
            except Exception as e:
                print(e)
                continue
        print(result)
        file = str(random.randint(1, 10000)) + '.data'
        with open(file, 'w') as fh:
            fh.write(json.dumps(result, ensure_ascii=False))
        print('文件名为{0}'.format(file))
if __name__ == '__main__':
    main()
