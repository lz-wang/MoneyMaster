#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: test_MoneyData.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/26 下午11:12
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from model.MoneyData import MonthData


class TestMoneyData(TestCase):
    # def setUp(self):
    #     self.mock_

    def test_MonthData(self):
        md = MonthData()
        mock_fetch_result = [('2020-12-01', '支出', 15.9), ('2020-12-02', '支出', 19)]
        md.from_sqlite(fetch_result=mock_fetch_result)

        self.assertEqual(len(md.data), len(mock_fetch_result))

