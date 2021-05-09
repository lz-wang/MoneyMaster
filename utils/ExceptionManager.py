#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: ExceptionManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/7 下午10:24


class DatabaseError(Exception):
    """数据库异常"""
    def __init__(self, err_msg):
        super().__init__(self)  # 初始化父类
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg


class ConfigError(Exception):
    """配置文件异常"""
    def __init__(self, err_msg):
        super().__init__(self)  # 初始化父类
        self.err_msg = err_msg

    def __str__(self):
        return self.err_msg



