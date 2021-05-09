#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AppChecker.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/8 下午11:27

import os

from utils.LogManager import MoenyLogger
from utils.SQLiteManager import MySqlite
from utils.ConfigManager import ConfigTool
from utils.ExceptionManager import DatabaseError, ConfigError
from model.WechatPayModel import WechatPayDatabase
from model.AliPayModel import AliPayDB


class Checker:
    def __init__(self):
        self.log = MoenyLogger().logger
        self.config = ConfigTool().cfg_reader()
        self.guard = Initializer()
        self.db_path = self.config['paths']['database']['main']

    def check_all(self):
        self.log.info('--- Ready to check APP ---')
        try:
            self.check_database()
            self.check_config()
        except DatabaseError as db_err:
            self.log.error(db_err)
            self.guard.init_database(self.db_path)
        except ConfigError:
            self.guard.init_config()
        self.log.info('--- Check APP SUCCESS ---')

    def check_database(self):
        self.log.info('--- Check APP Database ---')
        if not os.path.exists(self.db_path):
            raise DatabaseError('Dababase file %s doesn\'t exists' % self.db_path)
        else:
            app_db = MySqlite(self.db_path)
            app_db.connect_db()
            tables = app_db.show_all_table_name()
            if 'wechat' not in tables:
                self.guard.init_database_wechat(app_db)
            elif 'alipay' not in tables:
                self.guard.init_database_alipay(app_db)
        self.log.info('--- Check APP Database SUCESS ---')

    def check_config(self):
        pass


class Initializer:
    def __init__(self):
        self.log = MoenyLogger().logger

    def init_database(self, db_path):
        self.log.warning('init database...')
        app_db = MySqlite(db_path)
        app_db.connect_db()
        self.init_database_wechat(app_db)
        self.init_database_alipay(app_db)
        app_db.disconnect_db()

    def init_database_wechat(self, app_db):
        self.log.warning('init WechatPay database table')
        wechat = WechatPayDatabase()
        app_db.creat_table(wechat.table_name, wechat.table_attr)
        app_db.insert_data(wechat.table_name, wechat.test_data)
        # app_db.delete_table(wechat.table_name)
        self.log.info('init WechatPay database table SUCCESS')

    def init_database_alipay(self, app_db):
        self.log.warning('init AliPay database table')
        alipay = AliPayDB()
        app_db.creat_table(alipay.table_name, alipay.table_attr)
        app_db.insert_data(alipay.table_name, alipay.test_data)
        # app_db.delete_table(alipay.table_name)
        self.log.info('init AliPay database table SUCCESS')

    def init_config(self):
        pass
