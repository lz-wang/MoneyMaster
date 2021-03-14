#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataChart.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/15 上午12:15

import os
from datetime import datetime
from PyQt5.QtChart import (QChart, QChartView, QLineSeries, QSplineSeries,
                           QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QPushButton, QComboBox, QRadioButton, QCheckBox, QSpacerItem, QSizePolicy,
                             QDateTimeEdit, QDateEdit, QScrollBar)

from model.MoneyData import MonthData, YearData, AllYearsData
from utils.LogManager import MoenyLogger
from utils.SQLiteManager import MySqlite

PICK_ALL = '全部'
LINE_CHART = '折线图'
BAR_CHART = '柱状图'
MONEY_IN = '收入'
MONEY_OUT = '支出'
MONEY_OTHERS = '其他'
AXIS_DAY = '日期'
AXIS_MONTH = '月份'
AXIS_YEAR = '年份'
AXIS_MONEY = '金额'


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
            if str(self.chart_picker.currentText()) == BAR_CHART:
                self.view = BarChart()
            elif str(self.chart_picker.currentText()) == LINE_CHART:
                self.view = LineChart()
            self.view.set_data(data)

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
        self.year_picker.setCurrentText(PICK_ALL)
        self.month_picker.addItem(PICK_ALL)
        self.month_picker.setCurrentText(PICK_ALL)
        self.chart_picker.addItem(BAR_CHART)
        self.chart_picker.addItem(LINE_CHART)

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


class MoneyChart(QChartView):
    def __init__(self):
        super().__init__()
        self.log = MoenyLogger().logger

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


class BarChart(MoneyChart):
    def __init__(self):
        super().__init__()
        self.chart_title = BAR_CHART
        self.chart = QChart()
        self.chart.setTitle(self.chart_title)

    def set_data(self, data=None):
        del self.chart
        self.chart = QChart()

        set_in = QBarSet(MONEY_IN)
        set_out = QBarSet(MONEY_OUT)
        set_other = QBarSet(MONEY_OTHERS)
        category = []
        money_max = 0

        for single_data in data.data:
            date_label = single_data['date'].split('-')[-1]
            category.append(date_label)
            set_in.append(single_data['money_in'])
            set_out.append(single_data['money_out'])
            set_other.append(single_data['money_others'])
            money_max = max(money_max, max(list(single_data.values())[1:]))
        money_max = self.beautify_money_max(money_max)

        series = QBarSeries()
        series.append(set_out)
        series.append(set_in)
        series.append(set_other)
        self.chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(category)
        if isinstance(data, MonthData):
            axis_x.setTitleText(AXIS_DAY)
        elif isinstance(data, YearData):
            axis_x.setTitleText(AXIS_MONTH)
        elif isinstance(data, AllYearsData):
            axis_x.setTitleText(AXIS_YEAR)
        self.chart.setAxisX(axis_x, series)

        axis_y = QValueAxis()
        axis_y.setRange(0, money_max)
        axis_y.setTickCount(11)
        axis_y.setTitleText(AXIS_MONEY)
        self.chart.setAxisY(axis_y, series)

        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle(data.name)
        self.setChart(self.chart)


class LineChart(MoneyChart):
    """
    TODO: 待重构，重复代码过多
    """
    def __init__(self):
        super().__init__()
        self.chart_title = LINE_CHART
        self.chart = QChart()
        self.chart.setTitle(self.chart_title)
        # self.chart.legend().setVisible(True)
        # self.chart.legend().setAlignment(Qt.AlignBottom)

    def set_data(self, data=None):
        del self.chart
        self.chart = QChart()
        series_in = QLineSeries()
        series_in.setName(MONEY_IN)
        series_out = QLineSeries()
        series_out.setName(MONEY_OUT)
        series_others = QLineSeries()
        series_others.setName(MONEY_OTHERS)

        category = []
        money_max = 0

        for single_data in data.data:
            date_label = single_data['date'].split('-')[-1]
            category.append(date_label)
            series_in.append(int(date_label), single_data['money_in'])
            series_out.append(int(date_label), single_data['money_out'])
            series_others.append(int(date_label), single_data['money_others'])
            money_max = max(money_max, max(list(single_data.values())[1:]))
        money_max = self.beautify_money_max(money_max)

        self.chart.addSeries(series_in)
        self.chart.addSeries(series_out)
        self.chart.addSeries(series_others)

        axis_x = QBarCategoryAxis()
        axis_x.append(category)
        if isinstance(data, MonthData):
            axis_x.setTitleText(AXIS_DAY)
        elif isinstance(data, YearData):
            axis_x.setTitleText(AXIS_MONTH)
        elif isinstance(data, AllYearsData):
            axis_x.setTitleText(AXIS_YEAR)
        self.chart.setAxisX(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, money_max)
        axis_y.setTickCount(11)
        axis_y.setTitleText(AXIS_MONEY)
        self.chart.setAxisY(axis_y, series_in)

        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle(data.name)
        self.setChart(self.chart)