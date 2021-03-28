#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DatabaseView.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/27 下午9:25


import sys
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QDialog, QPushButton, QApplication, QHBoxLayout,
                             QVBoxLayout, QGroupBox, QGridLayout, QLabel, QSpacerItem, QSizePolicy)
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from ui.DataTable import MoneyTableWidget
from ui.TimeFilter import TimeFilterWidget
from utils.SQLiteManager import MySqlite
from utils.ConfigManager import ConfigTool


class DatabaseView(QWidget):
    data_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self._init_ui()
        self.data_signal.connect(self.refresh_ui)

    def refresh_ui(self, signal):
        self.data_table.set_table_data(data=signal[0], header=signal[1])

    def _init_ui(self):
        self._init_filter()
        self.db_view = QWidget()
        vbox = QVBoxLayout()

        hbox_filter = QHBoxLayout()
        self.data_review = QLabel('数据概要')
        self.btn_reverse = QPushButton('切换顺序')
        self.btn_reverse.clicked.connect(self.reverse_order)
        self.btn_refresh = QPushButton('刷新')
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_filter = QPushButton('过滤')
        self.btn_filter.clicked.connect(self.show_db_filter)
        hbox_filter.addWidget(self.data_review)
        hbox_filter.addStretch(1)
        hbox_filter.addWidget(self.btn_reverse)
        hbox_filter.addWidget(self.btn_filter)
        hbox_filter.addWidget(self.btn_refresh)

        self.data_table = MoneyTableWidget(50)

        vbox.addLayout(hbox_filter)
        vbox.addWidget(self.data_table)
        self.setLayout(vbox)
        # self.resize(500, 500)

    def _init_filter(self):
        self.db_filter = DatabaseFilter(self.data_signal)
        self.db_filter.setWindowModality(Qt.ApplicationModal)

    def reverse_order(self):
        self.data_table.total_data.reverse()
        self.data_table.set_table_data()

    def show_db_filter(self):
        self.db_filter.db.connect_db()
        self.db_filter.exec_()

    def refresh_data(self):
        pass


class DatabaseFilter(QDialog):
    def __init__(self, data_signal: pyqtSignal):
        super().__init__()
        self.data_singnal = data_signal
        self.__init_database()
        self.__init_parameters()
        self.__init_ui()

    def __init_database(self):
        ct = ConfigTool()
        db_path = ct.cfg_reader()['paths']['database']['main']
        self.db = MySqlite(db_path)
        self.db.connect_db()
        # self.db_tables = self.db.show_all_table_name()[0]

    def __init_parameters(self):
        tables = self.db.show_all_table_name()[0]
        self.cur_db_table = tables[0]  # TODO: read from database view
        self.cur_table_header = self.db.show_table_header(self.cur_db_table)
        time_range = self.db.query_date_range_of_all_data(tables[0])[0]
        self.start_time = datetime.strptime(time_range[0], '%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.strptime(time_range[1], '%Y-%m-%d %H:%M:%S')

    def __init_ui(self):
        time_hbox = QHBoxLayout()
        self.start_group, self.start_filter = self.add_time_filter(is_start=True)
        self.end_group, self.end_filter = self.add_time_filter(is_start=False)
        time_hbox.addStretch(1)
        time_hbox.addWidget(self.start_group)
        time_hbox.addStretch(1)
        time_hbox.addWidget(self.end_group)
        time_hbox.addStretch(1)

        btn_hbox = QHBoxLayout()
        self.btn_reset = QPushButton('重置过滤器')
        self.btn_reset.clicked.connect(self.reset_filter)
        self.btn_apply = QPushButton('应用')
        self.btn_apply.clicked.connect(self.apply_filter)
        self.btn_okay = QPushButton('确定')
        self.btn_okay.clicked.connect(self.confirm)
        self.btn_cancel = QPushButton('取消')
        self.btn_cancel.clicked.connect(self.cancel)
        btn_hbox.addWidget(self.btn_reset)
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(self.btn_apply)
        btn_hbox.addWidget(self.btn_okay)
        btn_hbox.addWidget(self.btn_cancel)

        main_vbox = QVBoxLayout()
        main_vbox.addStretch(1)
        main_vbox.addLayout(time_hbox)
        main_vbox.addStretch(1)
        main_vbox.addLayout(btn_hbox)
        self.setLayout(main_vbox)
        self.setFixedSize(400, 300)

    def reset_filter(self):
        self.start_filter.reset_ui()
        self.end_filter.reset_ui()

    def apply_filter(self):
        start_year = str(self.start_filter.year_combox.currentText())
        start_month = str(self.start_filter.month_combox.currentText())
        start_day = str(self.start_filter.day_combox.currentText())
        end_year = str(self.end_filter.year_combox.currentText())
        end_month = str(self.end_filter.month_combox.currentText())
        end_day = str(self.end_filter.day_combox.currentText())
        start_str = start_year + '-' + start_month + '-' + start_day + ' 00:00:00'
        end_str = end_year + '-' + end_month + '-' + end_day + ' 23:59:59'
        start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
        fetched_data = self.db.query_by_trans_time(self.cur_db_table, start, end)

        self.data_singnal.emit((fetched_data, self.cur_table_header))

    def confirm(self):
        self.apply_filter()
        self.db.disconnect_db()
        self.close()

    def cancel(self):
        self.db.disconnect_db()
        self.close()

    def add_time_filter(self, is_start=True):
        if is_start:
            desc = '开始时间'
            time_filter = TimeFilterWidget(self.start_time, self.end_time, False)
        else:
            desc = '结束时间'
            time_filter = TimeFilterWidget(self.start_time, self.end_time, True)

        time_filter_layout = QHBoxLayout()
        time_filter_layout.addWidget(time_filter)
        time_group_box = QGroupBox(desc)
        time_group_box.setLayout(time_filter_layout)

        return time_group_box, time_filter


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = DatabaseView()
    main_wnd.show()
    app.exec()
