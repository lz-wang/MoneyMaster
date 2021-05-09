#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: WechatPayManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午10:43

import csv
import re
import time

from model.WechatPayModel import WechatPayData, WechatPayDatabase
from utils.FilesManager import get_file_encoding


class WechatPayManager(object):
    def __init__(self):
        self.csv_head = None
        self.statistics = WechatPayData().statistics
        self.csv_data = list()
        self.db = WechatPayDatabase()

    def read_wechat_csv_data(self, file_name):
        self.csv_data = []
        encoding = get_file_encoding(file_name)

        with open(file_name, encoding=encoding) as f:
            self.csv_head = None
            f_csv = csv.reader(f)
            for row in f_csv:
                if self.csv_head is None:
                    self.find_statistics(row)
                else:
                    try:
                        _fmt_row0 = time.strptime(row[0], "%Y/%m/%d %H:%M")
                        row[0] = time.strftime("%Y-%m-%d %H:%M:%S", _fmt_row0)
                    except ValueError:
                        _fmt_row0 = time.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        row[0] = time.strftime("%Y-%m-%d %H:%M:%S", _fmt_row0)
                    except Exception as e:
                        raise Exception('Exception in read csv data, REASON: %s' % e)
                    row[5] = float(row[5][1:])
                    self.csv_data.append(row)
                if '-----' in row[0]:  # ----------------------微信支付账单明细列表
                    self.csv_head = next(f_csv)

        return self.csv_data

    def find_statistics(self, row_data):
        # 匹配方括号内的字符串
        p1 = re.compile(r'\[(.*?)]')
        # 匹配带有小数点的数字
        p2 = re.compile(r'\d+\.?\d*')

        for data in row_data:
            if data == '':
                continue
            if '微信昵称' in data:
                self.statistics['usr_name'] = re.findall(p1, data)[0]
            elif '起始时间' in data:
                self.statistics['start_time'] = re.findall(p1, data)[0]
                self.statistics['end_time'] = re.findall(p1, data)[1]
            elif '导出时间' in data:
                self.statistics['export_time'] = re.findall(p1, data)[0]
            elif '共' in data:
                self.statistics['trans_num'] = re.findall(p2, data)[0]
            elif '收入：' in data:
                self.statistics['income_num'] = re.findall(p2, data)[0]
                self.statistics['income_amount'] = re.findall(p2, data)[1]
            elif '支出：' in data:
                self.statistics['expense_num'] = re.findall(p2, data)[0]
                self.statistics['expense_amount'] = re.findall(p2, data)[1]
            elif '中性交易：' in data:
                self.statistics['other_num'] = re.findall(p2, data)[0]
                self.statistics['other_amount'] = re.findall(p2, data)[1]

        return self.statistics
