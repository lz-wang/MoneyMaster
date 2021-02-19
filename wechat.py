#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File: wechat.py
#  Project: MoneyMaster
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/19 下午10:47
import os
import csv
from mylog import Logger


class WechatManager:
    def __init__(self):
        self.log = Logger().logger
        self.csv_head = None
        pass

    def read_data(self, file_name):
        with open(file_name) as f:
            f_csv = csv.reader(f)
            # headers = next(f_csv)
            for row in f_csv:
                if self.csv_head is not None:
                    self.log.info(row)
                if row[0] == '----------------------微信支付账单明细列表--------------------':
                    self.csv_head = next(f_csv)

    def write_data(self):
        pass

    def clean_data(self):
        pass

    def join_data(self):
        pass


if __name__ == '__main__':
    print('')
    cur_path = os.getcwd()
    wechat_data = cur_path + '/data/wechat/wechat2020Q4.csv'
    wm = WechatManager()
    wm.log.info(wechat_data)
    wm.read_data(wechat_data)

