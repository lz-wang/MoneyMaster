#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: SQLiteManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/24 下午9:27
import os
import sqlite3


class MySqlite(object):
    """
    SQLite database API
    Reference: https://docs.python.org/zh-cn/3.8/library/sqlite3.html
    """
    def __init__(self, db_name: str):
        self.db_file_path = db_name
        self.con = None
        self.cur = None

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

        sql = 'INSERT INTO ' + table_name + \
              ' (' + _attr[0:-1] + \
              ') VALUES (' + _values[0: -1] + ')'
        self.execute_sql(sql)

    def insert_multi_data(self, table_name: str, data):
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
        sql = 'SELECT * FROM ' + table_name
        self.execute_sql(sql)
        return self.cur.fetchall()

    def execute_sql(self, sql: str):
        try:
            print('***** execute SQL: ' + sql)
            self.cur.execute(sql)
            self.con.commit()
            print('***** result: SUCCESS *****')
        except Exception as e:
            print('***** result: FAILED, REASON: %s' % e)


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
