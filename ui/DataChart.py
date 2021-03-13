#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataChart.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/7 上午1:28

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt

from model.MoneyData import MonthData, YearData
from utils.LogManager import MoenyLogger


class MoneyChartWidget(QChartView):
    def __init__(self, chart_title: str = 'Default'):
        super().__init__()
        self.log = MoenyLogger().logger
        self.chart_title = chart_title
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
        self.bar_chart.removeAllSeries()
        if isinstance(data, MonthData) or isinstance(data, YearData):
            set_in = QBarSet('收入')
            set_out = QBarSet('支出')
            set_other = QBarSet('其他')
            category = []
            moeny_max = 0
            for single_data in data.data:
                print(single_data)
                date_label = single_data['date'].split('-')[-1]
                category.append(date_label)
                set_in.append(single_data['money_in'])
                set_out.append(single_data['money_out'])
                set_other.append(single_data['money_others'])
                moeny_max = max(moeny_max, max(list(single_data.values())[1:]))
                print(moeny_max)
            if 10000 < moeny_max < 100000:
                moeny_max = (int(moeny_max/1000)+1)*1000
            elif 1000 < moeny_max < 10000:
                moeny_max = (int(moeny_max/100)+1)*100
            print(moeny_max)

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
            self.bar_chart.setAxisX(axis_x, series)
            axis_y = QValueAxis()
            axis_y.setRange(0, moeny_max)
            axis_y.setTickCount(10)
            axis_y.setTitleText('金额')
            self.bar_chart.setAxisY(axis_y, series)

        # self.bar_chart.createDefaultAxes()
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
