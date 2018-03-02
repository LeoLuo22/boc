import unittest
from statictics import LogAnalysis, Parser
from collections import Counter, OrderedDict

class TestStatistics(unittest.TestCase):
    def test_init(self):
        log = LogAnalysis('C:\\Users\\lh7167\\Documents\\SametimeFileTransfers')
        self.assertEqual(log.directory, 'C:\\Users\\lh7167\\Documents\\SametimeFileTransfers')

    def test_list_files(self):
        log = LogAnalysis('C:\\Users\\lh7167\\Documents\\SametimeFileTransfers')
        self.assertEqual(len(log.list_files()), 55)

    def test_example(self):
        pass

    def test_count_requests_by_day(self):
        log = LogAnalysis('E:\\logs')
        count = log.count_requests_by_day('E:/logs/example.txt')
        self.assertTrue(isinstance(count, dict))

    def test_count_by_interface(self):
        log = LogAnalysis('E:\\logs')
        count = log.count_by_interface('E:/logs/example.txt')
        self.assertTrue(isinstance(count, dict))

    def test_get_valid_requests(self):
        log = LogAnalysis('E:\\logs')
        count = log.get_valid_requests('E:/logs/example.txt')
        self.assertTrue(isinstance(count, list))

    def test_get_max_tbs(self):
        log = LogAnalysis('E:\\logs')
        items = log.get_valid_requests('E:/logs/example.txt')
        max_tps = log.get_max_tbs(items)
        self.assertTrue(isinstance(max_tps, tuple))
        self.assertEqual(max_tps[1], 14)
    def test_list_dates(self):
        a = {'daily': Counter({'25/Dec/2017': 4312112, '27/Dec/2017': 4128506, '26/Dec/2017': 4013800, '24/Dec/2017': 2613482, '28/Dec/2017': 1015238}), 'search_requests': OrderedDict([('24/Dec/2017', 278), ('25/Dec/2017', 430), ('26/Dec/2017', 440), ('27/Dec/2017', 496), ('28/Dec/2017', 162)]), 'max_tps': [('25/Dec/2017 16:34:31', 190), ('27/Dec/2017 16:04:20', 170), ('24/Dec/2017 15:54:35', 116), ('28/Dec/2017 10:22:56', 192), ('26/Dec/2017 10:17:55', 268)], 'open_requests': OrderedDict([('24/Dec/2017', 366752), ('25/Dec/2017', 592816), ('26/Dec/2017', 555328), ('27/Dec/2017', 570124), ('28/Dec/2017', 141156)]), 'login_requests': OrderedDict([('24/Dec/2017', 382876), ('25/Dec/2017', 666988), ('26/Dec/2017', 622774), ('27/Dec/2017', 637782), ('28/Dec/2017', 152598)])}
        results = dict(key='1', value=a)
        b = []
        b.append(results)
        parser = Parser(b)
        parser.list_days()

def main():
    a = {'daily': Counter({'25/Dec/2017': 4312112, '27/Dec/2017': 4128506, '26/Dec/2017': 4013800, '24/Dec/2017': 2613482, '28/Dec/2017': 1015238}), 'search_requests': OrderedDict([('24/Dec/2017', 278), ('25/Dec/2017', 430), ('26/Dec/2017', 440), ('27/Dec/2017', 496), ('28/Dec/2017', 162)]), 'max_tps': [('25/Dec/2017 16:34:31', 190), ('27/Dec/2017 16:04:20', 170), ('24/Dec/2017 15:54:35', 116), ('28/Dec/2017 10:22:56', 192), ('26/Dec/2017 10:17:55', 268)], 'open_requests': OrderedDict([('24/Dec/2017', 366752), ('25/Dec/2017', 592816), ('26/Dec/2017', 555328), ('27/Dec/2017', 570124), ('28/Dec/2017', 141156)]), 'login_requests': OrderedDict([('24/Dec/2017', 382876), ('25/Dec/2017', 666988), ('26/Dec/2017', 622774), ('27/Dec/2017', 637782), ('28/Dec/2017', 152598)])}
    results = dict(key='1', value=a)
    b = []
    b.append(results)
    parser = Parser(b)
    parser.daily_open_requests()
if __name__ == '__main__':
    main()
