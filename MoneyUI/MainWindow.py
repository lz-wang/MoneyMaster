#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MainWindow.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/27 上午12:05
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from MoneyUI.DataTable import MoneyTableWidget
from MoneyUI.TimeFilter import TimeFilterWidget
from WechatPay.WechatPayManager import DataManager


class MoenyMainWindow(QMainWindow):
    def __init__(self):
        super(MoenyMainWindow, self).__init__()
        self.wechat = DataManager()
        self.log = self.wechat.log
        self.__init_ui()

    def __init_ui(self):
        self.resize(1200, 800)
        self.setWindowTitle("数据库分页视图")
        # _db_data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        self.__init_money_table_widget()
        self.__init_time_filter_group()

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.table_widget)
        self.hbox.addWidget(self.time_widget)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hbox)
        # self.setLayout(self.hbox)
        self.setCentralWidget(self.main_widget)

    def __init_money_table_widget(self):
        # ds = datetime.datetime.strptime('2015-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        # de = datetime.datetime.strptime('2016-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        # _db_data = self.wechat.db.query_by_trans_time(table_name=self.wechat.wechat_db.table_name,
        #                                               dt_start=ds, dt_end=de)
        _db_data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        _table_head = list(self.wechat.wechat_db.table_attr.keys())
        self.table_widget = MoneyTableWidget(page_row=50, data=_db_data, head=_table_head)
        self.table_widget.set_page_controller()
        self.table_widget.control_signal.connect(self.page_controller)

    def __init_time_filter_group(self):
        self.__init_time_filter_widget()
        self.time_widget = QWidget()
        time_widget_title = QLabel('时间过滤器')
        time_widget_title.setAlignment(Qt.AlignHCenter)
        start_label = QLabel('开始时间')
        end_label = QLabel('结束时间')
        self.back_start = QPushButton('回到最早')
        self.back_start.clicked.connect()
        self.to_end = QPushButton('去向最近')

        grid = QGridLayout()
        grid.addWidget(time_widget_title, 1, 1, 1, 2)
        grid.addWidget(start_label, 2, 1)
        grid.addWidget(end_label, 2, 2)
        grid.addWidget(self.left_time_widget, 3, 1)
        grid.addWidget(self.right_time_widget, 3, 2)
        grid.addWidget(self.back_start, 4, 1)
        grid.addWidget(self.to_end, 4, 2)
        self.time_widget.setLayout(grid)

    def back_start(self):
        pass

    def to_end(self):
        pass

    def __init_time_filter_widget(self):
        data = self.wechat.db.query_min_max_trans_time(self.wechat.wechat_db.table_name)[0]
        self.start = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
        self.end = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
        self.left_time_widget = TimeFilterWidget(self.start, self.end, False)
        self.right_time_widget = TimeFilterWidget(self.start, self.end, True)

    def page_controller(self, signal):
        total_page = self.table_widget.page
        if "first_page" == signal[0]:
            self.table_widget.cur_page.setText("1")
        elif "pre_page" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.table_widget.cur_page.setText(str(int(signal[1]) - 1))
        elif "next_page" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.table_widget.cur_page.setText(str(int(signal[1]) + 1))
        elif "final_page" == signal[0]:
            self.table_widget.cur_page.setText(str(total_page))
        elif "skip_page" == signal[0]:
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.table_widget.cur_page.setText(signal[1])

        cur_page = int(self.table_widget.cur_page.text())
        self.update_table(page=cur_page)

    def update_table(self, page):
        self.table_widget.set_page_data(page)

    def read_db(self):
        self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
