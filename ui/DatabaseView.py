#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DatabaseView.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/27 下午9:25


import sys
from PyQt5.QtWidgets import QWidget, QDialog, QPushButton, QApplication, QHBoxLayout
from PyQt5.Qt import Qt
from ui.DataTable import MoneyTableWidget


class DatabaseView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        pass

    def _init_ui(self):
        self._init_filter()
        self.db_view = QWidget()

        self.btn_filter = QPushButton('过滤', self)
        self.btn_filter.clicked.connect(self.show_db_filter)
        self.btn_filter.move(50, 50)
        self.resize(500, 500)

    def _init_filter(self):
        self.db_filter = QDialog()
        btn_confirm = QPushButton('OK', self.db_filter)
        self.db_filter.setWindowModality(Qt.ApplicationModal)

    def show_db_filter(self):
        self.db_filter.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_wnd = DatabaseView()
    main_wnd.show()

    app.exec()
