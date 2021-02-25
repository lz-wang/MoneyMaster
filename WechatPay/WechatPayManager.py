#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: WechatPayManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/21 上午10:48
import csv
import os
import re
import time
import copy

from WechatPay.WechatPayModel import WechatPayData, WechatPayDB
from MoneyDB.SQLiteManager import MySqlite
from utils.mylog import Logger


class DataManager:
    def __init__(self):
        self.log = Logger(to_file=False).logger
        self.csv_head = None
        self.wechat_data = WechatPayData()
        self.wechat_db = WechatPayDB()
        self.db_path = os.path.join(os.getcwd(), 'data/database/'+self.wechat_db.db_name)
        self.db = MySqlite(self.db_path)
        self.db.connect_db()

    def read_csv_data(self, file_names_text):
        self.wechat_data.statistics.clear()
        self.wechat_data.data.clear()
        file_names = file_names_text.split('|')
        for file_name in file_names:
            print(file_name)
            with open(file_name) as f:
                self.csv_head = None
                f_csv = csv.reader(f)
                for row in f_csv:
                    if self.csv_head is None:
                        self.find_statistics(row)
                    else:
                        try:
                            _fmt_row0 = time.strptime(row[0], "%Y/%m/%d %H:%M")
                            row[0] = time.strftime("%Y-%m-%d %H:%M:%S", _fmt_row0)
                            print(row[0])
                        except:
                            pass
                        self.wechat_data.data.append(row)
                    if row[0][0:5] == '-----':  # ----------------------微信支付账单明细列表
                        self.csv_head = next(f_csv)
        print(self.wechat_data.data)

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

    def write_data_to_db(self, data):
        self.log.info('--WRITE to DB---')
        print(self.db_path)
        self.db.creat_table(self.wechat_db.table_name, self.wechat_db.table_attr)
        self.db.insert_data(self.wechat_db.table_name, data[1:])

    def clear_db_data(self):
        self.db.clear_table(self.wechat_db.table_name)

    def clean_data(self):
        pass

    def join_data(self):
        pass


if __name__ == '__main__':
    print('')
    data_path = os.path.join(os.getcwd(), '../data')
    wechat_data = data_path + '/wechat/wechat2020Q4.csv'
    wm = DataManager()
    wm.log.info(wechat_data)
    wm.read_csv_data(wechat_data)
