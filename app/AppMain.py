#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: AppMain.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/13 下午9:43

import sys
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import MoenyMainWindow


def run_app():
    app = QApplication(sys.argv)
    window = MoenyMainWindow()
    window.show()
    sys.exit(app.exec_())
