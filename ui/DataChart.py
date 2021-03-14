#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataChart.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/14 下午11:21

import os
from datetime import datetime
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QPushButton, QComboBox, QRadioButton, QCheckBox, QSpacerItem, QSizePolicy,
                             QDateTimeEdit, QDateEdit, QScrollBar)

from model.MoneyData import MonthData, YearData, AllYearsData
from utils.LogManager import MoenyLogger
from utils.SQLiteManager import MySqlite

PICK_ALL = '全部'


class MoneyChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.log = MoenyLogger().logger
        self.view = None
        self.db = MySqlite(os.path.join(os.getcwd(), 'data/database/money.db'))
        self.db.connect_db()
        self.__init_default_view()

    def __init_default_view(self):
        self.__init_chart_view()

        self.controller_layout = QHBoxLayout()
        self.__init_view_controller()

        self.gloabl_layout = QVBoxLayout()
        self.gloabl_layout.addLayout(self.controller_layout)
        self.gloabl_layout.addWidget(self.view)
        self.setLayout(self.gloabl_layout)

    def __init_view_controller(self):
        self.chart_label = QLabel()
        self.chart_label.setText('图表类型')
        self.chart_picker = QComboBox()

        self.account_label = QLabel()
        self.account_label.setText('账户')
        self.account_picker = QComboBox()

        self.date_label = QLabel()
        self.date_label.setText('范围')
        self.year_picker = QComboBox()
        self.year_picker.currentTextChanged.connect(self.change_month_picker)
        self.year_label = QLabel()
        self.year_label.setText('年')
        self.month_picker = QComboBox()
        self.month_label = QLabel()
        self.month_label.setText('月')

        self.init_combobox()

        self.search_btn = QPushButton()
        self.search_btn.setText('查询数据')
        self.search_btn.clicked.connect(self.search_data)

        self.controller_layout.addStretch(1)
        self.controller_layout.addWidget(self.chart_label)
        self.controller_layout.addWidget(self.chart_picker)
        self.controller_layout.addStretch(1)
        self.controller_layout.addWidget(self.account_label)
        self.controller_layout.addWidget(self.account_picker)
        self.controller_layout.addStretch(1)
        self.controller_layout.addWidget(self.date_label)
        self.controller_layout.addWidget(self.year_picker)
        self.controller_layout.addWidget(self.year_label)
        self.controller_layout.addWidget(self.month_picker)
        self.controller_layout.addWidget(self.month_label)
        self.controller_layout.addStretch(1)
        self.controller_layout.addWidget(self.search_btn)
        self.controller_layout.addStretch(1)

    def __init_chart_view(self):
        label = QLabel('请指定时间检索数据')
        label.setAlignment(Qt.AlignCenter)
        self.view = label

    def set_chart_view(self, data=None):
        if self.view:
            self.gloabl_layout.removeWidget(self.view)

        if data is None:
            self.view = QLabel('[%s] 数据异常，请重试！' % datetime.now())
        elif len(data.data) == 0:
            self.view = QLabel('[%s] 请求的日期范围无数据，请重试！' % datetime.now())
        else:
            self.view = BarChart()
            self.view.set_bar_chart_data(data)

        self.view.setAlignment(Qt.AlignCenter)
        self.gloabl_layout.addWidget(self.view)

    def init_combobox(self):
        db_tables = self.db.query_all_table_name()[0]
        for account in db_tables:
            self.account_picker.addItem(account)

        data = self.db.query_date_range_of_all_data('wechat')[0]
        start = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
        for y in range(start.year, end.year+1):
            self.year_picker.addItem(str(y))
        for m in range(12):
            self.month_picker.addItem(str(m+1))

        self.account_picker.addItem(PICK_ALL)
        self.year_picker.addItem(PICK_ALL)
        self.month_picker.addItem(PICK_ALL)
        self.chart_picker.addItem('柱状图')
        self.chart_picker.addItem('折线图')

    def search_data(self):
        data, fetched_data = None, None
        table = str(self.account_picker.currentText())
        year = str(self.year_picker.currentText())
        month = str(self.month_picker.currentText())
        if year != PICK_ALL and month != PICK_ALL:
            fetched_data = self.db.query_by_month_trans_time_data(table, int(year), int(month))
            data = MonthData()
            data.from_sqlite(fetched_data)
        elif year == PICK_ALL:
            fetched_data = self.db.query_by_all_years_trans_time_data(table)
            data = AllYearsData()
            print(data)
            data.from_sqlite(fetched_data)
        elif month == PICK_ALL:
            fetched_data = self.db.query_by_year_trans_time_data(table, int(year))
            data = YearData()
            data.from_sqlite(fetched_data)
        self.set_chart_view(data)

    def change_month_picker(self):
        if str(self.year_picker.currentText()) == PICK_ALL:
            self.month_picker.setEnabled(False)
        else:
            self.month_picker.setEnabled(True)


class BarChart(QChartView):
    def __init__(self):
        super().__init__()
        self.log = MoenyLogger().logger
        self.chart_title = '数据纵览'
        self.__init_line_chart()
        self.__init_bar_chart()

    def __init_line_chart(self):
        self.line_chart = QChart()
        self.line_chart.createDefaultAxes()
        self.line_chart.setTitle(self.chart_title)
        self.line_chart.legend().setVisible(True)
        self.line_chart.legend().setAlignment(Qt.AlignBottom)

    def set_line_chart_data(self, data=None):
        if isinstance(data, MonthData):
            series = QLineSeries()
            series.setName(data.name)
            for single_data in data.data:
                date_day = int(single_data['date'].split('-')[-1])
                money_type = single_data['type']
                money = single_data['money']
                if money_type == '支出':
                    series.append(date_day, money)

            self.line_chart.addSeries(series)
        self.line_chart.createDefaultAxes()
        self.setChart(self.line_chart)

    def __init_bar_chart(self):
        self.bar_chart = QChart()
        self.bar_chart.setTitle(self.chart_title)
        self.line_chart.legend().setVisible(True)
        self.line_chart.legend().setAlignment(Qt.AlignBottom)

    def set_bar_chart_data(self, data=None):
        del self.bar_chart
        self.__init_bar_chart()
        set_in = QBarSet('收入')
        set_out = QBarSet('支出')
        set_other = QBarSet('其他')
        category = []
        money_max = 0

        for single_data in data.data:
            print(single_data)
            date_label = single_data['date'].split('-')[-1]
            category.append(date_label)
            set_in.append(single_data['money_in'])
            set_out.append(single_data['money_out'])
            set_other.append(single_data['money_others'])
            money_max = max(money_max, max(list(single_data.values())[1:]))
            print(money_max)
        money_max = self.beautify_money_max(money_max)

        series = QBarSeries()
        series.append(set_out)
        series.append(set_in)
        series.append(set_other)

        self.bar_chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(category)
        if isinstance(data, YearData):
            axis_x.setTitleText('月份')
        elif isinstance(data, MonthData):
            axis_x.setTitleText('日期')
        elif isinstance(data, AllYearsData):
            axis_x.setTitleText('年份')
        self.bar_chart.setAxisX(axis_x, series)

        axis_y = QValueAxis()
        axis_y.setRange(0, money_max)
        axis_y.setTickCount(11)
        axis_y.setTitleText('金额')
        self.bar_chart.setAxisY(axis_y, series)

        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.bar_chart.setTitle(data.name)
        self.setChart(self.bar_chart)

    def __init_pie_chart(self):
        pass

    def draw_line_chart(self):
        pass

    def draw_bar_chart(self):
        pass

    def draw_pie_chart(self):
        pass

    @staticmethod
    def beautify_money_max(money_max: int):
        if 100 < money_max < 1000:
            money_max = (int(money_max / 100) + 1) * 100
        elif 1000 < money_max < 10000:
            money_max = (int(money_max / 1000) + 1) * 1000
        elif 10000 < money_max < 100000:
            money_max = (int(money_max / 10000) + 1) * 10000
        elif 100000 < money_max:
            money_max = (int(money_max / 100000) + 1) * 100000

        return money_max
