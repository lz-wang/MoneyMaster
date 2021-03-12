#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MainWindow.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/7 上午1:30
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QTabWidget, QMainWindow,
                             QPushButton, QLabel, QSpacerItem, QSizePolicy,
                             QMessageBox,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt
from MoneyUI.DataTable import MoneyTableWidget
from MoneyUI.DataChart import MoneyChartWidget, MoneyChartData
from MoneyUI.TimeFilter import TimeFilterWidget
from WechatPay.WechatPayManager import DataManager
from model.MoneyData import MonthData


class MoenyMainWindow(QMainWindow):
    def __init__(self):
        super(MoenyMainWindow, self).__init__()
        self.wechat = DataManager()
        self.log = self.wechat.log
        self.__init_ui()

    def __init_ui(self):
        self.resize(1200, 800)
        self.setWindowTitle("Money Master")
        # _db_data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        self.__init_money_table_widget()
        self.__init_line_chart_widget()
        self.__init_time_filter_group()
        self.__init_right_side()
        self.left_widget = QTabWidget()
        self.left_widget.addTab(self.table_widget, self.table_widget.windowTitle())
        self.left_widget.addTab(self.line_chart_widget, self.line_chart_widget.windowTitle())
        print(self.table_widget.windowTitle())

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.left_widget)
        self.hbox.addWidget(self.right_side)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.hbox)
        self.setCentralWidget(self.main_widget)

    def __init_money_table_widget(self):
        # ds = datetime.datetime.strptime('2015-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        # de = datetime.datetime.strptime('2016-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        # _db_data = self.wechat.db.query_by_trans_time(table_name=self.wechat.wechat_db.table_name,
        #                                               dt_start=ds, dt_end=de)
        _db_data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        _table_head = list(self.wechat.wechat_db.table_attr.keys())
        self.table_widget = MoneyTableWidget(page_row=100, data=_db_data, head=_table_head)
        self.table_widget.setWindowTitle("表格视图")
        # self.table_widget.set_page_controller()
        self.table_widget.control_signal.connect(self.page_controller)

    def __init_line_chart_widget(self):
        # self.line_chart_data = MoneyChartData()
        self.line_chart_widget = MoneyChartWidget()
        self.line_chart_widget.setWindowTitle('折线图')

    def __init_right_side(self):
        self.right_side = QWidget()
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_widget)
        vbox.addItem(verticalSpacer)
        self.right_side = QWidget()
        self.right_side.setLayout(vbox)

    def __init_time_filter_group(self):
        self.__init_time_filter_widget()
        self.time_widget = QWidget()

        time_widget_title = QLabel('===时间过滤器===')
        time_widget_title.setAlignment(Qt.AlignHCenter)
        start_label = QLabel('--开始时间--')
        start_label.setAlignment(Qt.AlignHCenter)
        end_label = QLabel('--结束时间--')
        end_label.setAlignment(Qt.AlignHCenter)

        self.back_start = QPushButton('回到最早')
        self.back_start.clicked.connect(self._back_start)
        self.to_end = QPushButton('去向最近')
        self.to_end.clicked.connect(self._to_end)
        self.change_order = QPushButton('切换顺序')
        self.change_order.clicked.connect(self._change_order)
        self.query_db = QPushButton('查询数据库')
        self.query_db.clicked.connect(self._query_db)
        self.test_btn_1 = QPushButton('TEST 1')
        self.test_btn_1.clicked.connect(self._test_1)

        grid = QGridLayout()
        grid.addWidget(time_widget_title, 1, 1, 1, 2)
        grid.addWidget(start_label, 2, 1)
        grid.addWidget(end_label, 2, 2)
        grid.addWidget(self.left_time_widget, 3, 1)
        grid.addWidget(self.right_time_widget, 3, 2)
        grid.addWidget(self.back_start, 4, 1)
        grid.addWidget(self.to_end, 4, 2)
        grid.addWidget(self.change_order, 5, 1)
        grid.addWidget(self.query_db, 5, 2)
        grid.addWidget(self.test_btn_1, 6, 1)
        self.time_widget.setLayout(grid)

    def _test_1(self):
        y, m = 2020, 11
        sql_result = self.wechat.db.query_by_month_trans_time_data(self.wechat.wechat_db.table_name, y, m)
        m_data = MonthData(str(y) + '年' + str(m) + '月 支出数据')
        print(sql_result)
        m_data.from_sqlite(sql_result)
        # self.line_chart_widget.set_line_chart_data(data=m_data)
        self.line_chart_widget.set_bar_chart_data(data=m_data)

    def _back_start(self):
        start_year = self.left_time_widget.start_year
        start_month = self.left_time_widget.start_month
        start_day = self.left_time_widget.start_day
        self.left_time_widget.year_combox.setCurrentText(str(start_year))
        self.left_time_widget.month_combox.setCurrentText(str(start_month))
        self.left_time_widget.day_combox.setCurrentText(str(start_day))

    def _to_end(self):
        end_year = self.right_time_widget.end_year
        end_month = self.right_time_widget.end_month
        end_day = self.right_time_widget.end_day
        self.right_time_widget.year_combox.setCurrentText(str(end_year))
        self.right_time_widget.month_combox.setCurrentText(str(end_month))
        self.right_time_widget.day_combox.setCurrentText(str(end_day))

    def _change_order(self):
        self.table_widget.total_data.reverse()
        self.table_widget.set_table_data()

    def _query_db(self):
        start_year = str(self.left_time_widget.year_combox.currentText())
        start_month = str(self.left_time_widget.month_combox.currentText())
        start_day = str(self.left_time_widget.day_combox.currentText())
        end_year = str(self.right_time_widget.year_combox.currentText())
        end_month = str(self.right_time_widget.month_combox.currentText())
        end_day = str(self.right_time_widget.day_combox.currentText())
        self.log.info('start: %s-%s-%s' % (start_year, start_month, start_day))
        self.log.info('end: %s-%s-%s' % (end_year, end_month, end_day))
        start_str = start_year + '-' + start_month + '-' + start_day + ' 00:00:00'
        end_str = end_year + '-' + end_month + '-' + end_day + ' 23:59:59'
        start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
        data = self.wechat.db.query_by_trans_time(self.wechat.wechat_db.table_name,
                                                  start, end)

        self.update_table(data=data)

    def __init_time_filter_widget(self):
        data = self.wechat.db.query_all_trans_time_data(self.wechat.wechat_db.table_name)[0]
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

    def update_table(self, page=None, data=None):
        if page is not None:
            self.table_widget.set_page_data(page)
        if data is not None:
            self.table_widget.set_table_data(data)

    def read_db(self):
        self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
