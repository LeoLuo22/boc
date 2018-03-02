import random
import datetime
import json
import os
from collections import OrderedDict
from collections import Counter

# 分成小函数的确优美 但是太慢太慢
class LogAnalysis:
    def __init__(self, directory):
        if not directory:
            directory = 'E:/logs/'+ str(datetime.date.today())
        self.directory = directory
        self.files = None

    def analysis(self, file):
        """
        统计，只遍历一次
        @return
        """
        tps = {} # 保存每秒请求数
        max_tps = [] # 保存每秒最大请求数
        dates = [] # 保存每天交易量
        search_dict = OrderedDict() # 保存搜索请求数
        login_dict = OrderedDict() # 保存登陆次数
        open_dict = OrderedDict() # 保存打开app次数

        with open(file, 'r') as fh:
            for line in fh:
                line = line.replace('\n', '')
                item = self.parse_line(line)
                if item:
                    _date = item.get('date')
                    interface = item.get('interface')
                    _time = _date +' '+item.get('hour')+':'+item.get('minute')+':'+item.get('second')
                    if _date not in tps:
                        tps[_date] = []
                    tps[_date].append(_time)
                    dates.append(_date) # 添加到dates
                    # 保存到接口统计列表
                    if _date not in search_dict.keys():
                        search_dict[_date] = 0
                        login_dict[_date] = 0
                        open_dict[_date] = 0
                    if interface == 'ubas030002':
                        search_dict[_date] = search_dict[_date] + 1
                    elif interface == 'ubas020007':
                        open_dict[_date] = open_dict[_date] + 1
                    elif interface == 'ubas020001':
                        login_dict[_date] = login_dict[_date] + 1
        """
        for key, value in tps.items():
            max_tps.append(max(Counter(value).items(), key=lambda x:x[1]))
        """
        return dict(tps=tps, daily=Counter(dates), search_requests=search_dict, open_requests=open_dict,
                    login_requests=login_dict)

    def get_valid_requests(self, file):
        """
        获取用户请求并保存在列表
        @param file
        @return
        [{'date': '24/Dec/2017', 'interface': 'images', 'method': 'GET', 'hour': '03', 'second': '02', 'minute': '06', 'status_code': '200'}]
        """
        items = []
        with open(file, 'r') as fh:
            for line in fh:
                line = line.replace('\n', '')
                item = self.parse_line(line)
                if item:
                    items.append(item)
        return items

    def get_datetimes(self, items):
        pass
    def get_max_tbs(self, items):
        """
        统计最大的并发交易量
        @param items 有效请求
        @return ('24/Dec/2017 03:07:09', 14)
        """
        tbs = []
        for item in items:
            # 24/Dec/2017-03:06:02
            date_time = item.get('date')+' '+item.get('hour')+':'+item.get('minute')+':'+item.get('second')
            tbs.append(date_time)

        return max(Counter(tbs).items(), key=lambda x:x[1])

    def count_by_search(self, items):
        """
        统计搜索接口调用次数
        @param items
        @return
        """
        result = self.count_by_interface(items)
        response = OrderedDict()
        for key, value in result.items():
            response[key] = dict(ubas030002=value.get('ubas030002'))
        return response

    def count_by_interface(self, items):
        """
        根据时间和接口类型统计
        @return OrderedDict([('24/Dec/2017', {'ubas020007': 102, 'ubas010001': 206, 'ubas000009': 4, 'ubas010002': 110, 'ubas010004': 2, 'ubas010003': 178, 'images': 64, 'ubas020001': 98, 'ubas020003': 22})])
        """

        response = OrderedDict()
        for item in items:
            date = result.get('date')
            interface = result.get('interface')
            if date not in response.keys():
                response[date] = {}
            if interface not in response[date].keys():
                response[date][interface] = 1
            else:
                response[date][interface] = response[date][interface] + 1
        return response

    def count_requests_by_day(self, items):
        """
        统计每天交易量，即GET和POST的
        @param file
        @return Counter({'24/Dec/2017': 786})
        """
        dates = []
        for item in items:
            dates.append(item.get('date'))
        return Counter(dates)

    def count_requests_by_search(self, items):
        """
        统计搜索功能使用次数
        @param items
        @return
        """
        interfaces = ['ubas030002']
        result = OrderedDict()
        for item in items:
            date = item.get('date')
            interface = item.get('interface')
            if interface in interfaces:
                if date in result:
                    result[date] = result[date]

    DeprecationWarning
    def remove_invalid(self, file):
        """
        去除文件中不是POST和GET方法的请求
        @return filename_clean
        """
        results = []
        total = 0 #Total requests
        with open(file, 'r') as fh:
            for line in fh:
                total += 1
                if self.is_valid_request(line):
                    results.append(line)
        print('Remove {0} invalid requests for {1}'.format(total-len(results), file))
        with open(file+'_clean', 'w') as fh:
            for result in results:
                fh.write(result)
        return file+'_clean'

    def list_files(self):
        """
        获取路径下所有文件,不包括文件夹
        @return list
        """
        results = []
        files = os.listdir(self.directory)
        for file in files:
            if not file.startswith('access'):
                continue
            path = os.path.join(self.directory, file)
            if os.path.isfile(path):
                results.append(path)

        return results

    def example(self, path=None, count=None):
        """
        生成示例文件，默认显示前1000条
        @param path 输出文件路径
        @param count 显示行数
        """
        self.list_files()
        if not count:
            count = 1000
        file = self.files[0]
        lines = []
        with open(file, 'r') as fd:
            _count = 0
            for line in fd:
                if _count > count:
                    break
                lines.append(line)
                _count += 1

        with open(self.directory+'/example.txt', 'w') as fh:
            for line in lines:
                fh.write(line)

    def parse_line(self, line):
        """
        处理每行日志
        @param line
        @return {'status_code': '200', 'date': '08/Jan/2018', 'interface': 'ubas010001', 'method': 'POST'}
        """
        valid_requests = ['POST', 'GET']
        splits = line.split(' ')
        method = splits[5].replace('"','')
        if method not in valid_requests:
            return False
        datetime = splits[3].split(':')
        date = datetime[0].replace('[','')
        hour = datetime[1]
        minute = datetime[2]
        second = datetime[3]

        interface = splits[6].split('/')[2]
        return dict(method=method, date=date, status_code=splits[8],
                interface=interface, hour=hour, minute=minute, second=second)

    def is_valid_request(self, line):
        """
        判断是否是POST或GET请求
        @return
        """
        valid_requests = ['POST', 'GET']
        splits = line.split(' ')
        method = splits[5].replace('"','')
        if method not in valid_requests:
            return False
        return True

    def count_by_all_day(self, results):
        """
        获取所有服务器上的交易量
        @param results
        @return
        """
        pass

class Parser:
    # 处理analysis返回的结果
    def __init__(self, results):
        # @param results list
        self.results = results

    def list_days(self):
        """
        获取结果里面所有日期
        @return {'28/Dec/2017', '24/Dec/2017', '26/Dec/2017', '25/Dec/2017', '27/Dec/2017'}
        """
        self.dates = set()
        for result in self.results:
            tmp = result.get('value')
            daily = tmp.get('daily')
            for k in daily.keys():
                self.dates.add(k)

    def daily_requests(self):
        """
        获取每天交易量
        @return {'24/Dec/2017': 2613482, '25/Dec/2017': 4312112, '26/Dec/2017': 4013800, '28/Dec/2017': 1015238, '27/Dec/2017': 4128506}
        """
        response = {}
        for result in self.results:
            daily = result.get('value').get('daily')
            for k, value in daily.items():
                if k not in response.keys():
                    response[k] = value
                else:
                    response[k] = response[k] + value
        return response

    def daily_login_requests(self):
        """
        获取每天登录数
        @return {'24/Dec/2017': 382876, '26/Dec/2017': 622774, '27/Dec/2017': 637782, '25/Dec/2017': 666988, '28/Dec/2017': 152598}
        """
        response = {}
        for result in self.results:
            daily = result.get('value').get('login_requests')
            for k, value in daily.items():
                if k not in response.keys():
                    response[k] = value
                else:
                    response[k] = response[k] + value
        return response

    def daily_search_requests(self):
        """
        获取每天搜索数
        @return {'25/Dec/2017': 430, '28/Dec/2017': 162, '24/Dec/2017': 278, '26/Dec/2017': 440, '27/Dec/2017': 496}
        """
        response = {}
        for result in self.results:
            daily = result.get('value').get('search_requests')
            for k, value in daily.items():
                if k not in response.keys():
                    response[k] = value
                else:
                    response[k] = response[k] + value
        return response

    def daily_open_requests(self):
        """
        获取每天打开次数
        @return {'28/Dec/2017': 141156, '27/Dec/2017': 570124, '25/Dec/2017': 592816, '26/Dec/2017': 555328, '24/Dec/2017': 366752}
        """
        response = {}
        for result in self.results:
            daily = result.get('value').get('open_requests')
            for k, value in daily.items():
                if k not in response.keys():
                    response[k] = value
                else:
                    response[k] = response[k] + value
        return response

    def daily_max_tps(self):
        """
        获取最大的tps
        @return
        """
        tps = {}
        max_tps = []
        for result in self.results:
            daily = result.get('value').get('tps')
            for key, value in daily.items():
                if key not in tps:
                    tps[key] = value
                else:
                    tps[key] = tps[key]+value
        for key, value in tps.items():
            max_tps.append(max(Counter(value).items(), key=lambda x:x[1]))
        return max_tps

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

def print_results(results):
    # 打印结果
    search_dict = OrderedDict()
    for result in results:
        tmp = result.get('value')
        search = tmp.get('search_requests')
        for k, v in search.items():
            if k not in search_dict:
                search_dict[k] = v
            else:
                search_dict[k] = search_dict[k] + v
    keys = search_dict.keys()
    for key in search_dict.keys():
        print('------{0}------'.format(key), end='')

    print('------------------------------------------')
    print('搜索请求数:', end='')
    for k in keys:
        print(search_dict.get(k), end=' ')


def main():
    print('===========日志统计V2.3=============')
    while True:
        directory = input('请输入文件目录（默认为E:\logs\当前日期)')
        results = []
        log = LogAnalysis(directory)
        try:
            files = log.list_files()
        except FileNotFoundError as e:
            print(e)
            print('请重新输入')
            continue
        for file in files:
            results.append(dict(key=file.replace(' ','').split('%'), value=log.analysis(file)))
        parser = Parser(results)
        print('每天交易量: {0}'.format(parser.daily_requests()))
        print('登陆次数: {0}'.format(parser.daily_login_requests()))
        print('APP打开次数: {0}'.format(parser.daily_open_requests()))
        print('搜索次数: {0}'.format(parser.daily_search_requests()))
        print('最高并发数: {0}'.format(parser.daily_max_tps()))


"""
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
"""
if __name__ == '__main__':
    main()
