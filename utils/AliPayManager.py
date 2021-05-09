#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AliPayManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午11:56

import csv
import re

from model.AliPayModel import AliPayData, AliPayDB
from utils.FilesManager import get_file_encoding


class AliPayManager:
    def __init__(self):
        self.csv_head = None
        self.statistics = AliPayData().statistics
        self.csv_data = list()
        self.db = AliPayDB()

    def read_alipay_csv_data(self, file_name):
        self.csv_data = list()
        need_record_data = False
        src_encoding = get_file_encoding(file_name)
        encoding = 'GBK' if src_encoding == 'GB2312' else src_encoding

        with open(file_name, encoding=encoding) as f:
            self.csv_head = None
            f_csv = csv.reader(f)
            for row in f_csv:
                if '-----' in row[0]:
                    if '交易记录明细列表' in row[0]:
                        self.csv_head = [s.strip() for s in next(f_csv)][:-1]
                        need_record_data = True
                    else:
                        need_record_data = False
                    continue
                if not need_record_data:
                    self.find_statistics(row)
                else:
                    self.csv_data.append(row[:-1])

        return self.csv_data

    def find_statistics(self, row_data):
        # 匹配方括号内的字符串
        p1 = re.compile(r'\[(.*?)]')
        # 匹配带有小数点的数字
        p2 = re.compile(r'\d+\.?\d*')

        for idx, data in enumerate(row_data):
            if data == '':
                continue
            if '账号' in data:
                self.statistics['account'] = re.findall(p1, data)[0]
            elif '起始日期' in data and '终止日期' in data:
                self.statistics['start_time'] = re.findall(p1, data)[0]
                self.statistics['end_time'] = re.findall(p1, data)[1]

            elif '共' in data:
                self.statistics['trans_num'] = re.findall(p2, data)[0]
            elif '已收入' in data:
                self.statistics['income_num'] = re.findall(p2, data)[0]
                self.statistics['income_amount'] = re.findall(p2, row_data[idx+1])[0]
            elif '待收入' in data:
                self.statistics['to_income_num'] = re.findall(p2, data)[0]
                self.statistics['to_income_amount'] = re.findall(p2, row_data[idx+1])[0]
            elif '已支出' in data:
                self.statistics['expense_num'] = re.findall(p2, data)[0]
                self.statistics['expense_amount'] = re.findall(p2, row_data[idx+1])[0]
            elif '待支出' in data:
                self.statistics['to_expense_num'] = re.findall(p2, data)[0]
                self.statistics['to_expense_amount'] = re.findall(p2, row_data[idx+1])[0]
            elif '导出时间' in data and '用户' in data:
                self.statistics['export_time'] = re.findall(p1, data)[0]

        return self.statistics


if __name__ == '__main__':
    test_csv = '/Users/lzwang/ZZ_AliPayData/支付宝 2013年.csv'
    apm = AliPayManager()
    apm.read_alipay_csv_data(test_csv)

    pass
