#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: mylog.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/2 上午12:38


import datetime
import logging
import os
import re

LOG_FILE_NAME = str(datetime.date.today()) + '.log'
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s, line.%(lineno)d]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class MoenyLogger(object):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename=LOG_FILE_NAME, level='debug', to_console=True, to_file=True):
        self.file_name = filename
        self.log_level = level
        self.to_file = to_file

        self.log_folder = self._init_log_folder()
        self.log_file = self.log_folder + '/' + self.file_name

        self.logger = logging.getLogger(self.log_file)
        self.logger.setLevel(self.level.get(level))  # 设置日志级别
        self._log_fmt = logging.Formatter(LOG_FORMAT)

        if not self.logger.handlers:
            # 设置屏幕输出
            if to_console:
                sh = logging.StreamHandler()
                sh.setFormatter(self._log_fmt)
                self.logger.addHandler(sh)

            # 设置文件输出
            # backupCount是文件的个数，如果超过这个个数，就会自动删除
            # interval是时间间隔，when是间隔的时间单位，单位有以下几种：
            # S 秒，M 分，H 小时，D 天，W 每星期（interval==0时代表星期一）
            # midnight 每天凌晨
            # th = handlers.TimedRotatingFileHandler(filename=log_file, when='midnight',
            #                                        backupCount=30, encoding='utf-8')
            # th.setFormatter(self._log_fmt)
            # self.logger.addHandler(th)

            # 以日期为名称的log文件输出
            if to_file:
                fh = logging.FileHandler(filename=self.log_file, encoding='utf-8')
                fh.setFormatter(self._log_fmt)
                self.logger.addHandler(fh)

    @staticmethod
    def _init_log_folder():
        cur_path = os.getcwd()
        project_root = re.findall(r'(.*?)MoneyMaster', cur_path)[0]
        log_folder = project_root + '/MoneyMaster/logs'
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        return log_folder
