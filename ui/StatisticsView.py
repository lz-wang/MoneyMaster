#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: StaticsView.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/28 下午4:49


from ui.DataTable import *
from PyQt5.QtWidgets import *


class StaticsView(QTabWidget):
    def __init__(self):
        super().__init__()


class DataFilter(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = StaticsView()
    main_wnd.show()
    app.exec()
