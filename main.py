#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: main.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/27 上午12:04
import sys
from MoneyUI.TestUi import run_gui
from MoneyUI.MoenyMainWindow import MoenyMainWindow, QApplication


if __name__ == '__main__':
    # run_gui()
    app = QApplication(sys.argv)
    window = MoenyMainWindow()
    window.show()
    sys.exit(app.exec_())

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
