#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: wechat.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/21 上午10:48
import os
import re
import csv
import datetime
from mylog import Logger


class WechatManager:
    def __init__(self):
        self.log = Logger(to_file=False).logger
        self.csv_head = None
        self.wechat_data = WechatPayData()
        pass

    def read_data(self, file_name):
        with open(file_name) as f:
            f_csv = csv.reader(f)
            # headers = next(f_csv)
            row_idx = 0
            for row in f_csv:
                if self.csv_head is None:
                    self.find_statistics(row)
                else:
                    self.log.info(row)
                    self.wechat_data.data.append(row)
                if row[0] == '----------------------微信支付账单明细列表--------------------':
                    self.csv_head = next(f_csv)
                    self.wechat_data.data.append(self.csv_head)
                row_idx += 1

        pass

    def find_statistics(self, row_data):
        # 匹配方括号内的字符串
        p1 = re.compile(r'[[](.*?)[]]', re.S)
        # \d+ 匹配1次或者多次数字
        # \.? 匹配小数点的，可能有，也可能没有
        # \d* 匹配小数点之后的数字
        p2 = re.compile(r'\d+\.?\d*')

        for data in row_data:
            if data == '':
                continue
            if data[0:4] == '微信昵称':
                self.wechat_data.statistics['usr_name'] = re.findall(p1, data)[0]
            elif data[0:4] == '起始时间':
                self.wechat_data.statistics['start_time'] = re.findall(p1, data)[0]
                self.wechat_data.statistics['end_time'] = re.findall(p1, data)[1]
            elif data[0:4] == '导出时间':
                self.wechat_data.statistics['export_time'] = re.findall(p1, data)[0]

            if data[0] == '共':
                self.wechat_data.statistics['trans_num'] = re.findall(p2, data)[0]
            elif data[0:2] == '收入':
                self.wechat_data.statistics['income_num'] = re.findall(p2, data)[0]
                self.wechat_data.statistics['income_amount'] = re.findall(p2, data)[1]
            elif data[0:2] == '支出':
                self.wechat_data.statistics['expense_num'] = re.findall(p2, data)[0]
                self.wechat_data.statistics['expense_amount'] = re.findall(p2, data)[1]
            elif data[0:2] == '中性':
                self.wechat_data.statistics['other_num'] = re.findall(p2, data)[0]
                self.wechat_data.statistics['other_amount'] = re.findall(p2, data)[1]

    def write_data(self):
        pass

    def clean_data(self):
        pass

    def join_data(self):
        pass


class WechatPayData(object):
    def __init__(self):
        self.statistics = {
            'usr_name': '',
            'start_time': '',
            'end_time': '',
            'export_time': '',
            'trans_num': 0,
            'income_num': 0,
            'income_amount': 0,
            'expense_num': 0,
            'expense_amount': 0,
            'other_num': 0,
            'other_amount': 0
        }
        self.data: list = []


if __name__ == '__main__':
    print('')
    cur_path = os.getcwd()
    wechat_data = cur_path + '/data/wechat/wechat2020Q4.csv'
    wm = WechatManager()
    wm.log.info(wechat_data)
    wm.read_data(wechat_data)
