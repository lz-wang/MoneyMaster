#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AppMain.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/19 上午12:32

import sys

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MoneyMainWindow


def run_app():
    app = QApplication(sys.argv)
    main_wnd = MoneyMainWindow()
    main_wnd.show()
    app.exec()
