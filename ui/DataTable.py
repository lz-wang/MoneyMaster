#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataTable.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/28 下午8:28

import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QLabel,
                             QLineEdit, QTableWidgetItem, QMessageBox)

from utils.ConfigManager import ConfigTool
from utils.LogManager import MoenyLogger
from utils.SQLiteManager import MySqlite


class MoneyTableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, page_row=20, data=None, header=None):
        super().__init__()
        self.log = MoenyLogger().logger
        self.cfg = ConfigTool().cfg_reader()
        self.page_row = page_row

        if data is None or header is None:
            self.setup_database()
        else:
            self.header = header
            self.total_data = data

        self.__init_main_ui()
        self.__init_data_table()
        self.__init_page_controller()
        self.control_signal.connect(self.page_controller)

    def __init_main_ui(self):
        self.table = QTableWidget()
        self.page_control_hbox = QHBoxLayout()

        self.global_layout = QVBoxLayout()
        self.global_layout.addWidget(self.table)
        self.global_layout.addLayout(self.page_control_hbox)
        self.setLayout(self.global_layout)
        table_style = self.load_style_sheet()
        self.setStyleSheet(table_style)

    def __init_data_table(self):
        self.total_row = len(self.total_data)
        self.total_col = len(self.total_data[0])
        self.page_col = self.total_col
        self.page = int(self.total_row / self.page_row) + 1
        self.page_data = []

        self.table.setRowCount(self.page_row)
        self.table.setColumnCount(self.page_col)
        self.table.setHorizontalHeaderLabels(self.header)
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
        self.skip_page_num = QLineEdit()
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
        self.page_control_hbox.addWidget(self.skip_page_num)
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

    def page_controller(self, signal):
        total_page = self.page
        btn_clicked = signal[0]
        target_page = int(signal[1])
        if btn_clicked == "first_page":
            self.cur_page.setText("1")
        elif btn_clicked == "pre_page":
            if target_page == 1:
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.cur_page.setText(str(target_page - 1))
        elif btn_clicked == "next_page":
            if target_page == total_page:
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.cur_page.setText(str(target_page + 1))
        elif btn_clicked == "final_page":
            self.cur_page.setText(str(total_page))
        elif btn_clicked == "skip_page":
            try:
                target_page = int(self.skip_page_num.text())
            except Exception as e:
                self.log.info('skip_page error, REASON: %s' % e)
                return
            if target_page < 0 or target_page > total_page:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.cur_page.setText(str(target_page))
        self.set_page_data(int(self.cur_page.text()))

    def set_page_data(self, page):
        if not 1 <= page <= self.page:
            return
        self.log.info('Go to page %d/%d' % (page, self.page))
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.header)
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

    def set_table_data(self, data=None, header=None):
        if header is not None:
            self.table.setHorizontalHeaderLabels(header)
        if data is not None:
            self.total_data = data
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.header)
        self.total_row = len(self.total_data)
        self.page = int(self.total_row/self.page_row) + 1
        self.cur_page.setText('1')
        self.total_page.setText("共" + str(self.page) + "页")
        self.__init_data_table()
        self.set_page_data(1)

    def show_total_page(self):
        return int(self.total_page.text()[1:-1])

    def setup_database(self, db_name='main'):
        db_path = self.cfg['paths']['database'][db_name]
        db = MySqlite(db_path)
        db.connect_db()
        db_tables = db.show_all_table_name()[0]
        if 'money' in db_tables:
            default_table = 'money'
        else:
            default_table = db_tables[0]
        self.total_data = db.query_all_data(default_table)
        self.header = db.show_table_header(default_table)
        db.disconnect_db()

    def load_style_sheet(self):
        style_sheet_qss = self.cfg['paths']['stylesheet']['TableStyle']
        with open(style_sheet_qss, 'r') as f:
            table_style = f.read()
        return table_style


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = MoneyTableWidget(page_row=50)
    main_wnd.show()
    app.exec()
