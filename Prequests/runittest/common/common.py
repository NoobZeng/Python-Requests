# !/usr/bin/env python
# ! _*_ coding:utf-8 _*_
# @TIME   : 2019/1/4  22:57
# @Author : Noob
# @File   : common.py

import re
import os
import yaml
import xlrd
import csv
from Prequests.runittest.common.logger import Log
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
log = Log()

class CommonTest:

    @staticmethod
    def login(s, username, password):
        url = 'http://127.0.0.1/zentao/user-login-L3plbnRhby8=.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        payload = {
            'account': username,
            'password': password,
            'referer': '/zentao/'
        }
        r = s.post(url, data=payload, headers=headers)
        try:
            pl = re.findall(r"location='(.+?)'", r.text)[0]
            assert '/zentao/' in pl
            log.info('成功登录!!!')
        except Exception as msg:
            log.error('登录失败：%s' % msg)

    @staticmethod
    def get_data(filename):
        cwd_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\data\\'
        file_path = os.path.join(cwd_path, filename)
        try:
            assert os.path.isfile(file_path)
        except AssertionError as msg:
            if filename == '':
                log.info('直接使用内部数据！！！')
                list_data = (['000', '000'], ['111', '111'])
                return list_data
            else:
                log.error('该文件不存在：%s' % msg)
        f = open(file_path, 'r', encoding='utf-8')
        if file_path.endswith('.yaml'):
            log.info('使用外部数据：%s' % filename)
            cfg = yaml.load(f)
            f.close()
            cfg.remove(cfg[0])
            return cfg
        elif file_path.endswith('.txt'):
            cfg = f.readlines()
            f.close()
            cfg.remove(cfg[0])
            rows = []
            for i in cfg:
                i = i.split(',')
                i[1] = i[1].rstrip('\n')
                rows.append(i)
            return rows
        elif file_path.endswith('.xlsx'):
            book = xlrd.open_workbook(file_path)
            sheet = book.sheet_by_index(0)
            rows = []
            for i in range(1, sheet.nrows):
                rows.append(sheet.row_values(i, 0, sheet.ncols))
                for j in rows:
                    j[1] = int(j[1])
            return rows
        elif file_path.endswith('.csv'):
            cfg = csv.reader(f)
            f.close()
            next(cfg, None)
            rows = []
            for i in cfg:
                rows.append(i)
            return rows
        else:
            return '不支持该类型文件'

    @staticmethod
    def send_email(sender, psw, receiver, smtpserver, port, report_file):
        """
        发送最新的测试报告
        :param sender: 发送人账号
        :param psw: 除了QQ使用授权码外，其他使用正常的密码
        :param receiver: 接收人
        :param smtpserver: 邮箱服务
        :param port: 邮箱端口号
        :param report_file: 最新的测试报告
        :return:
        """

        # f = open(report_file, 'rb')
        # mail_body = f.read()
        # f.close()
        with open(report_file, 'rb') as f:
            mail_body = f.read()
            f.close()

        # 邮件类型为"multipart/mixed"的邮件包含附件。向上兼容，如果一个邮件有纯文本正文，超文本正文，内嵌资源，附件，则选择mixed类型。
        # MIMEMultipart对象代表邮件本身
        msg = MIMEMultipart('mixed')

        # 附件
        msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
        msg_html1['Content-Disposition'] = 'attachment;filename="TestReport.html"'
        msg_html1['Content-Type'] = 'Application/octet-stream'
        msg.attach(msg_html1)

        # 邮件正文
        msg_html = MIMEText(mail_body, 'html', 'utf-8')
        msg.attach(msg_html)

        # 使用三个引号来设置邮件信息，标准邮件需要三个头部信息： From, To, 和 Subject ，每个信息直接使用空行分割
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = u'自动化测试报告'
        try:
            try:
                smtp = smtplib.SMTP_SSL(smtpserver, port)
            except:
                smtp = smtplib.SMTP()
                smtp.connect(smtpserver, port)
            smtp.login(sender, psw)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            log.info('邮件成功发送给%s' % receiver)
        except smtplib.SMTPException:
            log.error('邮件发送失败！！！')