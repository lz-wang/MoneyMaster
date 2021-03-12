#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataChart.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/7 上午1:28
import random  # TODO: test only, to be removed
import sys

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from model.MoneyData import MonthData


class MoneyChartData(object):
    def __init__(self):
        self.source: str = ''
        self.data: dict = {}  # {'in': 20, '}

    def add_data(self, label: str = None, data: list = None):
        if label is None:
            label = 'NULL'
        self.data[label] = data


class MoneyChartWidget(QChartView):
    def __init__(self, chart_title: str = 'Default'):
        super().__init__()
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
        if isinstance(data, MonthData):
            set_out = QBarSet('支出')
            set_in = QBarSet('收入')
            catg = []
            for single_data in data.data:
                date_day = single_data['date'].split('-')[-1]
                catg.append(date_day)
                money_type = single_data['type']
                money = single_data['money']
                if money_type == '支出':
                    set_out.append(money)
                else:
                    set_in.append(money)
            series = QBarSeries()
            series.append(set_out)
            series.append(set_in)

            self.bar_chart.addSeries(series)
            axis = QBarCategoryAxis()
            axis.append(catg)
            self.bar_chart.setAxisX(axis, series)
        self.bar_chart.createDefaultAxes()
        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.setChart(self.bar_chart)

    def __init_pie_chart(self):
        pass

    def draw_line_chart(self):
        pass

    def draw_bar_chart(self):
        pass

    def draw_pie_chart(self):
        pass

    def mock_data(self):
        for i in range(3):
            fake_data = [random.randint(0, 50) for _ in range(31)]
            self.data['Month-' + str(i)] = fake_data


def test():
    mcd = MoneyChartData()
    for i in range(3):
        fake_data = [random.randint(0, 50) for _ in range(31)]
        mcd.add_data(label='Month-'+str(i), data=fake_data)

    app = QApplication(sys.argv)
    mcw = MoneyChartWidget(chart_data=None)
    mcw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
