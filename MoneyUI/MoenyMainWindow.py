#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MoenyMainWindow.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/27 上午12:05
from PyQt5.QtWidgets import *
from MoneyUI.DataTable import MoneyTableWidget
from WechatPay.WechatPayManager import DataManager


class MoenyMainWindow(QMainWindow):
    def __init__(self):
        super(MoenyMainWindow, self).__init__()
        self.wechat = DataManager()
        self.log = self.wechat.log
        self.__init_ui()

    def __init_ui(self):
        self.resize(1700, 900)
        self.setWindowTitle("数据库分页视图")
        _db_data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        _table_head = list(self.wechat.wechat_db.table_attr.keys())
        self.table_widget = MoneyTableWidget(page_row=50, data=_db_data, head=_table_head)
        self.table_widget.set_page_controller()
        self.table_widget.control_signal.connect(self.page_controller)
        self.setCentralWidget(self.table_widget)

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
