#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午9:53


import re

from utils.LogManager import MoenyLogger
from utils.SQLiteManager import MySqlite
from utils.ConfigManager import ConfigTool
from utils.WechatPayManager import WechatPayManager
from utils.AliPayManager import AliPayManager
from utils.AppChecker import Initializer


class DataManager(object):
    def __init__(self):
        self.log = MoenyLogger().logger
        self.cfg = ConfigTool().cfg_reader()
        self.csv_head = None
        self.db_path = self.cfg['paths']['database']['main']
        self.db = MySqlite(self.db_path)

    def read_data(self, data_type, data_file):
        file_type = self.get_file_type(data_file)
        self.log.info(f'Get data: file name is {data_file}, data type is {data_type}.')
        if data_type == '微信':
            wechat = WechatPayManager()
            if file_type == 'csv':
                wechat.read_wechat_csv_data(data_file)
            else:
                raise TypeError(f'Known wechat data file type: {file_type}')
            data, review = wechat.csv_data, wechat.statistics
        elif data_type == '支付宝':
            alipay = AliPayManager()
            if file_type == 'csv':
                alipay.read_alipay_csv_data(data_file)
            else:
                raise TypeError(f'Known wechat data file type: {file_type}')
            data, review = alipay.csv_data, alipay.statistics
        else:
            data, review = None, None

        return data, review

    def reset_databse(self):
        self.db.connect_db()
        self.db.delete_db()
        db_reseter = Initializer()
        db_reseter.init_database(self.db_path)

    def write_data_to_db(self, data, data_type):
        if data_type == '微信':
            table = WechatPayManager().db.table_name
        elif data_type == '支付宝':
            table = AliPayManager().db.table_name
        else:
            raise TypeError(f'Known data type: {data_type}')

        self.log.warning(f'--- Write data to database [{self.db_path}], table is {table}')
        self.db.connect_db()
        self.db.insert_data(table, data[1:])
        self.db.disconnect_db()

    @staticmethod
    def get_file_type(file_name):
        pattern = re.compile(r'\.[A-Za-z0-9]+$')
        results = pattern.findall(file_name)

        return results[-1][1:] if results != [] else None
