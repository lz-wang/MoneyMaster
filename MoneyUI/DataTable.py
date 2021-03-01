#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataTable.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/27 下午10:19
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from MoneyUI.MoneyStyle import MONEY_TABLE_STYLE


class MoneyTableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, page_row=20, data=None, head=None):
        super().__init__()
        self.head = head
        self.total_data = data
        self.total_row = len(data)
        self.total_col = len(data[0])
        self.page_row = page_row
        self.page_col = self.total_col
        self.page = int(self.total_row/self.page_row) + 1
        self.page_data = []
        self.table = QTableWidget()
        self.page_control_hbox = QHBoxLayout()
        self.global_layout = QVBoxLayout()
        self.global_layout.addWidget(self.table)
        self.global_layout.addLayout(self.page_control_hbox)
        self.setLayout(self.global_layout)
        self.setStyleSheet(MONEY_TABLE_STYLE)
        self.__init_data_table()
        self.__init_page_controller()

    def __init_data_table(self):
        self.table.setRowCount(self.page_row)
        self.table.setColumnCount(self.page_col)
        self.table.setHorizontalHeaderLabels(self.head)
        self.table.setShowGrid(True)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.set_page_data(1)

    def __init_page_controller(self):
        self.first_page = QPushButton("首页")
        self.pre_page = QPushButton("<上一页")
        self.cur_page = QLabel("1")
        self.next_page = QPushButton("下一页>")
        self.final_page = QPushButton("尾页")
        self.total_page = QLabel("共" + str(self.page) + "页")
        self.skip_lable_0 = QLabel("跳到")
        self.skip_page = QLineEdit()
        self.skip_label_1 = QLabel("页")
        self.confirm_skip = QPushButton("确定")
        
        self.first_page.clicked.connect(self._first_page)
        self.pre_page.clicked.connect(self._pre_page)
        self.next_page.clicked.connect(self._next_page)
        self.final_page.clicked.connect(self._final_page)
        self.confirm_skip.clicked.connect(self._skip_page)

        self.page_control_hbox.addStretch(1)
        self.page_control_hbox.addWidget(self.first_page)
        self.page_control_hbox.addWidget(self.pre_page)
        self.page_control_hbox.addWidget(self.cur_page)
        self.page_control_hbox.addWidget(self.next_page)
        self.page_control_hbox.addWidget(self.final_page)
        self.page_control_hbox.addWidget(self.total_page)
        self.page_control_hbox.addWidget(self.skip_lable_0)
        self.page_control_hbox.addWidget(self.skip_page)
        self.page_control_hbox.addWidget(self.skip_label_1)
        self.page_control_hbox.addWidget(self.confirm_skip)
        self.page_control_hbox.addStretch(1)

    def _first_page(self):
        self.control_signal.emit(["first_page", self.cur_page.text()])

    def _pre_page(self):
        self.control_signal.emit(["pre_page", self.cur_page.text()])

    def _next_page(self):
        self.control_signal.emit(["next_page", self.cur_page.text()])

    def _final_page(self):
        self.control_signal.emit(["final_page", self.cur_page.text()])

    def _skip_page(self):
        self.control_signal.emit(["skip_page", self.cur_page.text()])

    def set_page_data(self, page):
        if not 1 <= page <= self.page:
            return
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.head)
        row_start = self.page_row * (page - 1)
        row_end = row_start + self.page_row
        cur_page_row = self.page_row
        if row_end > self.total_row:
            cur_page_row = self.page_row - (row_end - self.total_row) - 1
            row_end = self.total_row

        page_data = self.total_data[row_start:row_end]
        for r in range(cur_page_row):
            for c in range(self.page_col):
                item = QTableWidgetItem(str(page_data[r][c]))
                self.table.setItem(r, c, item)

    def set_table_data(self, data=None):
        if data is not None:
            self.total_data = data
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.head)
        self.total_row = len(self.total_data)
        self.page = int(self.total_row/self.page_row) + 1
        self.cur_page.setText('1')
        self.total_page.setText("共" + str(self.page) + "页")
        self.__init_data_table()
        self.set_page_data(1)

    def show_total_page(self):
        return int(self.total_page.text()[1:-1])
