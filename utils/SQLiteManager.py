#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: SQLiteManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/7 下午11:29

import datetime
import os
import sqlite3
import traceback

from utils.LogManager import MoenyLogger


class MySqlite(object):
    """
    SQLite database API
    Reference: https://docs.python.org/zh-cn/3.8/library/sqlite3.html
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.con = None
        self.cur = None
        self.log = MoenyLogger().logger

    def connect_db(self):
        """连接数据库"""
        self.con = sqlite3.connect(database=self.db_path)
        self.cur = self.con.cursor()

    def disconnect_db(self):
        """断开数据库"""
        self.cur.close()
        self.con.close()
        self.con = None
        self.cur = None

    def delete_db(self):
        """删除数据库文件"""
        if self.con is not None:
            self.disconnect_db()
        try:
            os.remove(self.db_path)
            self.log.warning('Delete database [%s] SUCCESS.' % self.db_path.split('/')[-1])
        except Exception as e:
            self.log.error('Delete database [%s] FAILED, REASON: %s' % (self.db_path.split('/')[-1], e))

    def creat_table(self, table_name: str, table_attr: dict):
        """创建数据库表"""
        _sql = 'CREATE TABLE ' + table_name + ' ('
        for k, v in table_attr.items():
            _sql += k + ' ' + v + ', '
        sql = _sql[0:-2] + ')'
        self.execute_sql(sql)

    def delete_table(self, table_name: str):
        """清空数据库表所有数据"""
        sql = 'DELETE FROM ' + table_name
        self.execute_sql(sql)

    def drop_table(self, table_name: str):
        """删除数据库表"""
        sql = 'DROP TABLE ' + table_name
        self.execute_sql(sql)

    def insert_data(self, table_name: str, data):
        """向指定数据库表写入单条或多条数据"""
        if isinstance(data, dict):
            self.insert_single_data(table_name, data)
        elif isinstance(data, list) or isinstance(data, tuple):
            self.insert_multi_data(table_name, data)
        else:
            raise Exception('insert data error')

    def insert_single_data(self, table_name: str, data: dict):
        """
        向指定数据库表写入单条数据\n
        data --> 必须为字典类型
        """
        _attr = ''
        _values = ''
        for k, v in data.items():
            _attr += (k + ',')
            _values += ('\'' + str(v) + '\',')

        sql = 'INSERT INTO ' + table_name + ' (' + _attr[0:-1] + ') VALUES (' + _values[0: -1] + ')'
        self.execute_sql(sql)

    def insert_multi_data(self, table_name: str, data):
        """
        插入多条数据\n
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
        """
        索引指定表的全部数据
        """
        sql = 'SELECT * FROM ' + table_name + ' ORDER BY trans_time DESC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_by_trans_time(self, table_name: str, dt_start=None, dt_end=None):
        """
        查询给定时间段索的数据\n
        dt --> datetime (format: %Y-%m-%d %H:%M:%S)
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

    def query_by_month_trans_time_data(self, table_name: str, year: int = 2020, month: int = 1):
        """
        查询指定月份的数据，统计每天支出或收入的总额
        """
        _year = str(year)
        _month = '0'+str(month) if month < 10 else str(month)
        sql = 'SELECT strftime(\'%Y-%m-%d\', trans_time), type, SUM(money) FROM ' + table_name + \
              ' WHERE strftime(\'%Y%m\', trans_time)=\'' + _year + _month + \
              '\' GROUP BY strftime(\'%Y%m%d\', trans_time), type ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_by_year_trans_time_data(self, table_name: str, year: int = 2020):
        """
        查询指定年份的数据，统计每月支出或收入的总额
        """
        sql = 'SELECT strftime(\'%Y-%m\', trans_time), type, SUM(money) FROM ' + table_name + \
              ' WHERE strftime(\'%Y\', trans_time)=\'' + str(year) + \
              '\' GROUP BY strftime(\'%Y%m\', trans_time), type ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_by_all_years_trans_time_data(self, table_name: str):
        """
        查询全部数据，统计每一年支出或收入的总额
        """
        sql = 'SELECT strftime(\'%Y\', trans_time), type, SUM(money) FROM ' + table_name + \
              ' GROUP BY strftime(\'%Y\', trans_time), type ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def query_date_range_of_all_data(self, table_name: str):
        """
        查询所有账单数据的时间范围
        """
        sql = 'SELECT MIN(trans_time), MAX(trans_time) FROM ' + table_name + ' ORDER BY trans_time ASC'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def show_all_table_name(self):
        """
        查询数据库的所有表
        """
        sql = 'SELECT name FROM sqlite_master WHERE type =\'table\''
        self.execute_sql(sql)
        raw_result = self.cur.fetchall()
        result = []
        for table in raw_result:
            result.append(table[0])
        return result

    def show_table_info(self, table_name: str):
        """
        获取指定表的所有列属性
        """
        sql = 'PRAGMA TABLE_INFO([' + table_name + '])'
        self.execute_sql(sql)
        return self.cur.fetchall()

    def show_table_header(self, table_name: str):
        """
        获取指定表的所有列字段信息\n
        :param table_name: 数据库表的名称
        :return: 指定数据库表的列字段名称
        """
        table_info = self.show_table_info(table_name)
        return [col[1] for col in table_info]

    def execute_sql(self, sql: str):
        """
        执行特定的数据库语句\n
        :param sql: 数据库语句
        :return: None
        """
        try:
            self.log.info('***** EXECUTE SQLite: ' + sql)
            self.cur.execute(sql)
            self.con.commit()
            self.log.info('***** SQLite RESULT: SUCCESS *****')
        except Exception as e:
            self.log.warning('***** SQLite RESULT: FAILED, REASON: %s' % e)
            traceback.print_exc()


if __name__ == '__main__':
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
    db.delete_table(table_name=t_name)

    # 删除表
    db.drop_table(table_name=t_name)

    # 断开数据库连接
    db.disconnect_db()

    # 删除数据库文件
    db.delete_db()
