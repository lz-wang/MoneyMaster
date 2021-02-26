#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataTable.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/27 上午12:04
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal


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
        self.__init_ui()

    def __init_ui(self):
        style_sheet = """
            QPushButton{
                max-width: 18ex;
                max-height: 6ex;
                font-size: 11px;
            }
            QLineEdit{
                max-width: 30px
            }
        """
        self.table = QTableWidget()
        self.table.setRowCount(self.page_row)
        self.table.setColumnCount(self.page_col)
        self.table.setHorizontalHeaderLabels(self.head)
        self.table.setShowGrid(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应宽度
        self.set_page_data(1)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet(style_sheet)

        self.skip_page = QLineEdit()
        self.cur_page = QLabel("1")
        self.total_page = QLabel("共" + str(self.page) + "页")

    def set_page_controller(self):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        skipLable_0 = QLabel("跳到")
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定")

        homePage.clicked.connect(self._first_page)
        prePage.clicked.connect(self._pre_page)
        nextPage.clicked.connect(self._next_page)
        finalPage.clicked.connect(self._final_page)
        confirmSkip.clicked.connect(self._skip_page)

        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.cur_page)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.total_page)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skip_page)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)

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

    def show_total_page(self):
        return int(self.total_page.text()[1:-1])