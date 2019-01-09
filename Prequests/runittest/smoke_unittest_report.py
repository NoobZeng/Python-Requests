# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/5  17:09
# @Author : Noob
# @File   : smoke_unittest_report.py

import HTMLTestRunner
import unittest
import os
# from Prequests.runittest.case.first_unittest import ZantaoTestFirst
# from Prequests.runittest.case.second_unittest import ZentaoTestSecond
from Prequests.runittest.common.logger import Log
from Prequests.runittest.common.common import CommonTest
from Prequests.runittest.config import readConfig

log = Log()

# first = unittest.TestLoader().loadTestsFromTestCase(ZantaoTestFirst)
# second = unittest.TestLoader().loadTestsFromTestCase(ZentaoTestSecond)

# test_suite = unittest.TestSuite()
# test_suite.addTest(first)
# test_suite.addTest(second)


base_path = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(base_path, 'report')

case_path = os.path.join(base_path, 'case')
discover = unittest.defaultTestLoader.discover(case_path, pattern='*unittest.py', top_level_dir=None)

if not os.path.exists(report_path):
    log.info('创建测试报告文件目录！！！')
    os.mkdir(report_path)

file_path = report_path + '/smoke_report.html'
outfile = open(file_path, 'wb+')
runner = HTMLTestRunner.HTMLTestRunner(
    stream=outfile,
    title='Test Report',
    description='smoke test'
)

if __name__ == '__main__':
    log.info('---测试开始---')
    # runner.run(test_suite)
    runner.run(discover)
    log.info('开始发送邮件')
    CommonTest.send_email(readConfig.sender, readConfig.psw, readConfig.receiver, readConfig.smtp_server, readConfig.port, file_path)
    log.info('---测试结束---')