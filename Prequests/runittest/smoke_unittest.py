# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/5  16:59
# @Author : Noob
# @File   : smoke_unittest.py

import unittest
from Prequests.runittest.case.first_unittest import ZantaoTestFirst
from Prequests.runittest.case.second_unittest import ZentaoTestSecond

first = unittest.TestLoader().loadTestsFromTestCase(ZantaoTestFirst)
second = unittest.TestLoader().loadTestsFromTestCase(ZentaoTestSecond)

smoke_tests = unittest.TestSuite()
smoke_tests.addTest(first)
smoke_tests.addTest(second)

unittest.TextTestRunner(verbosity=2).run(smoke_tests)