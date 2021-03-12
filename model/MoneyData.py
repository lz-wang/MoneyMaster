#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MoneyData.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/12 下午11:21
import re


class MoneyData(object):
    def __init__(self, name='MONEY_DATA'):
        self.name = name
        self.data = None
        self.date_type = '%Y-%m-%d %H:%M:%S'

    def from_sqlite(self, fetch_result=None, reload=True):
        if not fetch_result:
            return
        if reload:
            self.data.clear()

        for data in fetch_result:
            single_data = {
                'date': data[0],
                'type': data[1],
                'money': data[2]
            }
            self.data.append(single_data)


class MonthData(MoneyData):
    def __init__(self, name='MONTH_DATA'):
        super().__init__()
        self.name = name
        self.date_type = '%Y-%m-%d'
        self.data = []



