#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AppMain.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午10:47

import sys

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MoneyMainWindow
from utils.AppChecker import Checker


def run_app():
    app = QApplication(sys.argv)
    app_ui = MoneyMainWindow()
    app_ui.show()
    app.exec()


def check_app():
    app_checker = Checker()
    app_checker.check_all()
