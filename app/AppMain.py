#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AppMain.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/26 下午9:32

import sys

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MoenyMainWindow
from ui.TestUI import *


def run_app():
    app = QApplication(sys.argv)
    app_window = MoenyMainWindow()
    app_window.show()
    sys.exit(app.exec_())
