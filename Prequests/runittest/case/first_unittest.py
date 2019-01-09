# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/3  16:54
# @Author : Noob
# @File   : first_unittest.py

import requests
import unittest
from Prequests.runittest.common.common import CommonTest
import warnings
from bs4 import BeautifulSoup
from ddt import ddt, data, unpack
from Prequests.runittest.common.logger import Log

"""
1. 以禅道为例
"""

@ddt
class ZantaoTestFirst(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Log().info(u'%s的测试用例测试开始' % __class__.__name__)
        cls.session = requests.session()

    @data(*CommonTest.get_data('login_data.yaml'))
    @unpack
    def test_a(self, username, password):
        Log().info(u'登录测试开始')
        CommonTest.login(requests, username, password)

    def test_b(self):
        # 获取首页最新动态消息
        Log().info(u'获取最新的动态消息')
        CommonTest.login(self.session, 'xxx', 'xxx')
        base_url = 'http://127.0.0.1'
        url = 'http://127.0.0.1/zentao/my/'
        self.session.headers.update()
        r = self.session.get(url)
        try:
            soup = BeautifulSoup(r.text, features='html.parser')
            tag = soup.find(id='block2')
            r2 = self.session.get(base_url + tag['data-url'])
            soup2 = BeautifulSoup(r2.text, features='html.parser')
            try:
                for i in soup2.find_all('td'):
                    Log().info(i.get_text())
            except:
                Log().error(u'没有找到该td标签')
        except Exception as msg:
            Log().error(u'登录失败或其他：%s' % msg)

    @classmethod
    def tearDownClass(cls):
        Log().info(u'%s的测试用例测试结束' % __class__.__name__)

if __name__ == '__main__':
    unittest.main(verbosity=2)
