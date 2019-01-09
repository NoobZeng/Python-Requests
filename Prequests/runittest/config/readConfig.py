# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/6  18:15
# @Author : Noob
# @File   : readConfig.py

import os
import configparser

cur_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(cur_path, 'cfg.ini')
conf = configparser.ConfigParser()
conf.read(configPath, encoding='utf-8')

smtp_server = conf.get('email', 'smtp_server')
sender = conf.get('email', 'sender')
psw = conf.get('email', 'psw')
receiver = conf.get('email', 'receiver')
port = conf.get('email', 'port')