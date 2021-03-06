#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: main.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/7 上午12:14
import sys
from PyQt5.QtWidgets import QApplication
from MoneyUI.TestUi import run_gui
from MoneyUI.MainWindow import MoenyMainWindow


if __name__ == '__main__':
    # run_gui()
    app = QApplication(sys.argv)
    window = MoenyMainWindow()
    window.show()
    sys.exit(app.exec_())

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
