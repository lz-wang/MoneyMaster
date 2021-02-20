#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File: mylog.py
#  Project: MoneyMaster
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/20 上午12:09


import logging
from logging import handlers
import datetime
import os

LOG_FOLDER = "/logs"
LOG_FILE_NAME = str(datetime.date.today()) + '.log'
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s, line.%(lineno)d]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Logger(object):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename=LOG_FILE_NAME, level='debug'):
        log_path = os.getcwd() + LOG_FOLDER
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = log_path + '/' + filename

        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(self.level.get(level))  # 设置日志级别
        self._log_fmt = logging.Formatter(LOG_FORMAT)

        # 设置屏幕输出
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
        fh = logging.FileHandler(filename=log_file, encoding='utf-8')
        fh.setFormatter(self._log_fmt)
        self.logger.addHandler(fh)


if __name__ == '__main__':
    try:
        ml = Logger()
        ml.logger.debug('hello debug')
        ml.logger.info('hello info')
        ml.logger.warning('hello warning')
        ml.logger.error('hello error')
        ml.logger.critical('hello critical')
    except Exception as e:
        print(e)
