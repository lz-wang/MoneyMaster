#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MoneyData.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/14 下午11:21
import re


class MoneyData(object):
    def __init__(self, name='MONEY_DATA'):
        self.name = name
        self.data = []
        self.date_type = '%Y-%m-%d %H:%M:%S'

    def from_sqlite(self, fetch_result=None, reload=True):
        if not fetch_result:
            return None
        if reload:
            self.data.clear()
        init_data = {
            'date': 'error_date',
            'money_in': 0,
            'money_out': 0,
            'money_others': 0
        }

        for data in fetch_result:
            _date = data[0]
            _type = data[1]
            _money = round(data[2], 3)
            if self.data == [] or self.data[-1]['date'] != _date:
                self.add_date_data(_date)
            self.set_money_data(_type, _money)

        return self.data

    def add_date_data(self, date):
        init_data = {
            'date': 'error_date',
            'money_in': 0,
            'money_out': 0,
            'money_others': 0
        }

        self.data.append(init_data)
        self.data[-1]['date'] = date

    def set_money_data(self, money_type, money):
        if money_type == '收入':
            self.data[-1]['money_in'] = money
        elif money_type == '支出':
            self.data[-1]['money_out'] = money
        elif money_type == '/':
            self.data[-1]['money_others'] = money


class MonthData(MoneyData):
    def __init__(self, name='MONTH_DATA'):
        super().__init__()
        self.name = name
        self.date_type = '%Y-%m-%d'
        self.data = []


class YearData(MoneyData):
    def __init__(self, name='YEAR_DATA'):
        super().__init__()
        self.name = name
        self.date_type = '%Y-%m'
        self.data = []


class AllYearsData(MoneyData):
    def __init__(self, name='ALLYEAR_DATA'):
        super().__init__()
        self.name = name
        self.date_type = '%Y'
        self.data = []
