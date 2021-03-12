#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: SQLiteManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/6 下午11:54
import os
import sqlite3
import datetime
from utils.mylog import Logger


class MySqlite(object):
    """
    SQLite database API
    Reference: https://docs.python.org/zh-cn/3.8/library/sqlite3.html
    """
    def __init__(self, db_name: str):
        self.db_file_path = db_name
        self.con = None
        self.cur = None
        self.log = Logger().logger

    def connect_db(self):
        self.con = sqlite3.connect(database=self.db_file_path)
        self.cur = self.con.cursor()

    def disconnect_db(self):
        self.cur.close()
        self.con.close()
        self.con = None
        self.cur = None

    def delete_db(self):
        if self.con is not None:
            self.disconnect_db()
        try:
            os.remove(self.db_file_path)
            print('WARNING: Delete database [%s] SUCCESS.' %
                  self.db_file_path.split('/')[-1])
        except Exception as e:
            print('WARNING: Delete database [%s] FAILED, REASON: %s' %
                  (self.db_file_path.split('/')[-1], e))

    def creat_table(self, table_name: str, table_attr: dict):
        _sql = 'CREATE TABLE ' + table_name + ' ('
        for k, v in table_attr.items():
            _sql += k + ' ' + v + ', '
        sql = _sql[0:-2] + ')'
        self.execute_sql(sql)

    def clear_table(self, table_name: str):
        sql = 'DELETE FROM ' + table_name
        self.execute_sql(sql)

    def drop_table(self, table_name: str):
        sql = 'DROP TABLE ' + table_name
        self.execute_sql(sql)

    def insert_data(self, table_name: str, data):
        if isinstance(data, dict):
            self.insert_single_data(table_name, data)
        elif isinstance(data, list) or isinstance(data, tuple):
            self.insert_multi_data(table_name, data)
        else:
            raise Exception('insert data error')

    def insert_single_data(self, table_name: str, data: dict):
        _attr = ''
        _values = ''
        for k, v in data.items():
            _attr += (k + ',')
            _values += ('\'' + str(v) + '\',')

        sql = 'INSERT INTO ' + table_name + ' (' + _attr[0:-1] + ') VALUES (' + _values[0: -1] + ')'
        self.execute_sql(sql)

    def insert_multi_data(self, table_name: str, data):
        """
        插入多条数据
        data --> 可迭代的list或tuple
        """
        for r in data:
            _values = ''
            for v in r:
                _values += ('\'' + str(v) + '\',')
            sql = 'INSERT INTO ' + table_name + ' VALUES (' + _values[0: -1] + ')'
            self.execute_sql(sql)

    def delete_data(self):
        pass

    def update_data(self):
        pass

    def query_data(self, table_name: str, condition):
        pass

    def query_all_data(self, table_name: str):
        """索引指定表的全部数据"""
        sql = 'SELECT * FROM ' + table_name + ' ORDER BY trans_time DESC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_by_trans_time(self, table_name: str, dt_start=None, dt_end=None):
        """
        根据时间段索引数据
        dt --> datetime --> fmt: %Y-%m-%d %H:%M:%S
        """
        if dt_start is None:
            start = '2000-01-01 00:00:00'
        else:
            start = dt_start.strftime('%Y-%m-%d %H:%M:%S')
        if dt_end is None:
            end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            end = dt_end.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'SELECT * FROM ' + table_name + ' WHERE trans_time BETWEEN \'' + \
              start + '\' and \'' + end + '\' ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_by_month_trans_time_data(self, table_name: str, year: int = None, month: int = 1):
        """
        索引指定月份的数据，统计每天支出或收入的总额
        """
        if year is None:
            year = 2020
        sql = 'SELECT strftime(\'%Y-%m-%d\', trans_time), type, SUM(money) FROM ' + table_name + \
              ' WHERE strftime(\'%Y%m\', trans_time)=\'' + str(year) + str(month) + \
              '\' GROUP BY strftime(\'%Y%m%d\', trans_time), type'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_all_trans_time_data(self, table_name: str):
        """索引全部交易时间的数据"""
        sql = 'SELECT MIN(trans_time), MAX(trans_time) FROM ' + table_name + ' ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def execute_sql(self, sql: str):
        try:
            self.log.info('***** EXECUTE MYSQL: ' + sql)
            self.cur.execute(sql)
            self.con.commit()
            self.log.info('***** MySQL RESULT: SUCCESS *****')
        except Exception as e:
            self.log.warning('***** MySQL RESULT: FAILED, REASON: %s' % e)


if __name__ == '__main__':
    print('')

    # 连接 or 创建数据库
    db_file = os.getcwd() + '/test.db'
    db = MySqlite(db_file)
    db.connect_db()

    # 新建表
    t_name = 'person'
    t_attr = {
        'name': 'VARCHAR(20) DEFAULT NULL',
        'age': 'SMALLINT(2) DEFAULT NULL ',
        'sex': 'VARCHAR(8) DEFAULT NULL'
    }
    db.creat_table(table_name=t_name, table_attr=t_attr)

    # 插入单条数据
    record = {
        'name': 'daidai',
        'age': 15,
        'sex': 'male'
    }
    db.insert_data(table_name=t_name, data=record)  # 全属性
    record.pop('age')
    db.insert_data(table_name=t_name, data=record)  # 部分属性

    # 插入多条数据
    records = [('duoduo', '22', 'female'),
               ('dingding', '18', 'male')]
    db.insert_data(table_name=t_name, data=records)

    # 清空表数据
    db.clear_table(table_name=t_name)

    # 删除表
    db.drop_table(table_name=t_name)

    # 断开数据库连接
    db.disconnect_db()

    # 删除数据库文件
    db.delete_db()
