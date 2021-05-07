#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: WechatPayModel.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/8 上午12:25

class WechatPayData(object):
    def __init__(self):
        self.statistics = {
            'usr_name': '',       # 微信昵称
            'start_time': '',     # 起始时间
            'end_time': '',       # 终止时间
            'export_type': '',    # 导出类型
            'export_time': '',    # 导出时间
            'trans_num': 0,       # 记录总数
            'income_num': 0,      # 收入记录数
            'income_amount': 0,   # 收入金额
            'expense_num': 0,     # 支出记录数
            'expense_amount': 0,  # 支出金额
            'other_num': 0,       # 中性交易记录数
            'other_amount': 0,    # 中性交易金额
        }
        self.data: list = []


class WechatPayDB(object):
    def __init__(self):
        self.table_name = 'wechat'
        self.table_attr = {
            'trans_time': 'DATETIME NOT NULL',      # 交易时间
            'trans_type': 'VARCHAR(64) NOT NULL',   # 交易类型
            'trans_obj': 'VARCHAR(128) NOT NULL',   # 交易对方
            'commodity': 'VARCHAR(128) NOT NULL',   # 商品
            'type': 'VARCHAR(16) NOT NULL',         # 收支类型
            'money': 'INT(11) NOT NULL',            # 金额
            'pay_method': 'VARCHAR(64) NOT NULL',   # 支付方式
            'status': 'VARCHAR(64) NOT NULL',       # 当前状态
            'trans_id': 'VARCHAR(64) NOT NULL',     # 交易单号
            'merchant_id': 'VARCHAR(64) NOT NULL',  # 商户单号
            'readme': 'VARCHAR(128) NOT NULL',      # 备注
        }

        self.test_data = {
            'trans_time': '2019/12/31 16:54:47',
            'trans_type': '商户消费',
            'trans_obj': '蜜雪冰城',
            'commodity': '销售单',
            'type': '支出',
            'money': 25,
            'pay_method': '工商银行(8888)',
            'status': '支付成功',
            'trans_id': 4200000782942012315746749070,
            'merchant_id': 1167798210211201231146827955,
            'readme': '/',
        }
