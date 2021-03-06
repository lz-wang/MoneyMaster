#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DataChart.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/7 上午12:22
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QSplineSeries, QScatterSeries, QValueAxis

import sys, random  # TODO: test only, to be removed


class MoneyChartData(object):
    def __init__(self):
        self.data: dict = {}

    def add_data(self, label: str = None, data: list = None):
        if label is None:
            label = 'NULL'
        self.data[label] = data


class MoneyChartWidget(QChartView):
    def __init__(self, chart_data: MoneyChartData = None):
        super().__init__()
        self.data: dict = {}
        if chart_data:
            self.data = chart_data.data
        else:
            self.mock_data()
        # self.resize(800, 600)
        # self.chart_view = QChartView(self)
        # self.chart_view.resize(1200, 800)
        self.__init_line_chart(data=self.data)

    def __init_line_chart(self, data: dict):
        self.line_chart = QChart()
        for label, values in data.items():
            self.add_line_chart_data(label, values)
        # axis_x = QValueAxis()
        # axis_x.setRange(0, 31)
        # axis_x.setTickCount(31)
        # axis_x.applyNiceNumbers()
        # axis_x.setTitleText('DAY')
        #
        # axis_y = QValueAxis()
        # axis_y.setRange(-10, 60)
        # axis_y.setTitleText('RMB')
        # self.line_chart.setAxisX(axis_x)
        # self.line_chart.setAxisY(axis_y)

        self.line_chart.createDefaultAxes()
        self.line_chart.setTitle('Month Data')
        self.line_chart.legend().setVisible(True)
        self.line_chart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.line_chart)
        pass

    def add_line_chart_data(self, name: str, data: list):
        series = QLineSeries()
        series.setName(name)
        for idx, value in enumerate(data):
            series.append(idx, value)
        self.line_chart.addSeries(series)

    def __init_bar_chart(self):
        pass

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
