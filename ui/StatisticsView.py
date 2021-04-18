#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: StatisticsView.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/19 上午12:32

import sys
from ui.DataChart import MoneyChartWidget
from PyQt5.QtWidgets import *


class StaticsView(QTabWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        self.addTab(MoneyChartWidget('BAR_CHART'), '柱状图')
        self.addTab(MoneyChartWidget('LINE_CHART'), '折线图')


class DataFilter(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = StaticsView()
    main_wnd.show()
    app.exec()
