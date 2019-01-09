# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/4  0:53
# @Author : Noob
# @File   : second_unittest.py

import requests
import unittest
from Prequests.runittest.common.common import CommonTest
import re
from bs4 import BeautifulSoup
import datetime
from ddt import ddt, data, unpack
from Prequests.runittest.common.logger import Log

log = Log()

@ddt
class ZentaoTestSecond(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.info(u'%s开始执行测试用例' % __class__.__name__)
        cls.session = requests.session()
        CommonTest.login(cls.session, 'xxx', 'xxx')

    @data(*CommonTest.get_data('create_data.yaml'))
    @unpack
    def test_c(self, typename, title):
        # 新建测试用例
        self.session.headers.update()
        url = 'http://127.0.0.1/zentao/testcase-create-1-0-0.html'
        payload = {
            'product': '1',
            'branch': '0',
            'module': '0',
            'type': typename,
            'title': title,
            'pri': '1',
            'stepType[1]': 'item',
            'stepType[2]': 'item',
            'stepType[3]': 'item'
        }
        r = self.session.post(url, data=payload)
        try:
            lurl = re.findall(r"location='(.+?)'", r.text)[0]
            base_url = 'http://127.0.0.1'
            self.session.headers.update()
            r2 = self.session.get(base_url + lurl)
            soup = BeautifulSoup(r2.content.decode('utf-8'), features='html.parser')
            soup_text = []
            # 至少匹配一个数值：find_all(attrs={'data-id': re.compile(r'.\d+')})
            # 匹配所有含有data-id的tag：find_all(attrs={'data-id': True)
            for i in soup.find_all(attrs={'data-id': re.compile(r'.\d+')}):
                soup_text.append(i.get_text())
            now_time = datetime.datetime.now().strftime('%m-%d %H:%M')
            try:
                assert now_time in soup_text[0], '测试用例创建失败'
                log.info(soup_text[0])
                log.info(u'测试用例创建成功')
            except Exception as msg:
                log.error(u'测试用例创建失败：%s' % msg)
        except Exception as msg:
            log.error(u'当前数据获取失败：%s' % msg)

    @data(*CommonTest.get_data('search_data.yaml'))
    @unpack
    def test_d(self, typename, title):
        # 搜索测试用例
        self.session.headers.update()
        url = 'http://127.0.0.1/zentao/search-buildQuery.html'
        payload = {
            'fieldtitle': 'ZERO',
            'fieldpri': '3',
            'fieldproduct': '1',
            'andOr1': 'AND',
            'field1': 'title',
            'operator1': typename,
            'value1': title,
            'actionURL': '/zentao/testcase-browse-1-0-bySearch-myQueryID.html',
            'module': 'testcase',
            'formType': 'lite',
            'fieldlastRunResult': 'n/a'
        }
        base_url = 'http://127.0.0.1'
        r = self.session.post(url, data=payload)
        self.session.headers.update()
        try:
            lurl = re.findall(r"location='(.+?)'", r.text)[0]
            r2 = self.session.get(base_url + lurl, headers=self.session.headers)
            soup = BeautifulSoup(r2.content.decode('utf-8'), features='html.parser')
            try:
                j = 0
                for i in soup.find_all(attrs={'data-id': re.compile(r'.*\d')}):
                    j = j + 1
                    log.info(i.get_text())
                assert j >= 1
            except Exception as msg:
                log.error(u'该测试用例不存在：%s' % msg)
            log.info(u'成功搜索')
        except Exception as msg:
            log.error(u'返回数据错误：%s' % msg)

    @classmethod
    def tearDownClass(cls):
        log.info(u'%s结束执行测试用例' % __class__.__name__)

if __name__ == '__main__':
    unittest.main(verbosity=2)