#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AliPayModel.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/7 下午11:43


class AliPayData(object):
    def __init__(self):
        self.statistics = {
            'account': '',           # 账号
            'start_time': '',        # 起始日期
            'end_time': '',          # 终止日期
            'trans_num': 0,          # 记录总数
            'income_num': 0,         # 已收入记录数
            'income_amount': 0,      # 已收入金额
            'to_income_num': 0,      # 待收入记录数
            'to_income_amount': 0,   # 待收入金额
            'expense_num': 0,        # 已支出记录数
            'expense_amount': 0,     # 已支出金额
            'to_expense_num': 0,     # 待支出记录数
            'to_expense_amount': 0,  # 待支出金额
            'export_time': '',       # 导出时间
            'usr_name': '',          # 用户
        }
        self.data: list = []


class AliPayDB(object):
    def __init__(self):
        self.table_name = 'alipay'
        self.table_attr = {
            'trans_id': 'VARCHAR(64) NOT NULL',           # 交易号
            'merchant_id': 'VARCHAR(64) DEFAULT NULL',    # 商家订单号
            'trans_create_time': 'DATETIME NOT NULL',     # 交易创建时间
            'trans_pay_time': 'DATETIME DEFAULT NULL',    # 付款时间
            'trans_modify_time': 'DATETIME NOT NULL',     # 最近修改时间
            'trans_place': 'VARCHAR(64) NOT NULL',        # 交易来源地
            'trans_type': 'VARCHAR(64) NOT NULL',         # 类型
            'trans_obj': 'VARCHAR(128) NOT NULL',         # 交易对方
            'commodity': 'VARCHAR(256) NOT NULL',         # 商品名称
            'money': 'REAL(11) NOT NULL',                 # 金额（元）
            'type': 'VARCHAR(16) DEFAULT NULL',           # 收/支
            'trans_status': 'VARCHAR(64) NOT NULL',       # 交易状态
            'service_money': 'REAL(11) NOT NULL',         # 服务费（元）
            'refund_money': 'REAL(11) NOT NULL',          # 成功退款（元）
            'readme': 'VARCHAR(128) DEFAULT NULL',        # 备注
            'money_status': 'VARCHAR(128) DEFAULT NULL',  # 资金状态
        }

        self.test_data = {
            'trans_id': '2020111122001426201419764174',
            'merchant_id': 'MM97PLKWY5c1',
            'trans_create_time': '2020-11-11 14:28:05',
            'trans_pay_time': '2020-11-11 14:28:06',
            'trans_modify_time': '2020-11-11 14:28:06',
            'trans_place': '其他（包括阿里巴巴和外部商家）',
            'trans_type': '即时到账交易',
            'trans_obj': 'iCloud 由云上贵州运营',
            'commodity': 'App Store & Apple Music: 于 11.10完成的购买',
            'money': 21.00,
            'type': '支出',
            'trans_status': '交易成功',
            'service_money': 0.00,
            'refund_money': 0.00,
            'readme': '',
            'money_status': '已支出 ',
        }
