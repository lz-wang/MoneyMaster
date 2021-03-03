
import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QValueAxis, QBarCategoryAxis


class MoneyLineChart(QMainWindow):
    def __init__(self, data: list, attr: dict):
        super().__init__()
        self.data = data
        self.attr = attr
        self.__init_widget()
        self.__init_chart()

    def __init_widget(self):
        self.setWindowTitle('折线图')
        self.resize(1200, 800)

    def __init_chart(self):
        self.line_chart = QChart()
        self.line_chart.setTitle('Month Data')
        self.chart_view = QChartView(self)
        self.chart_view.setChart(self.line_chart)
        self.setCentralWidget(self.chart_view)

        self.series = QLineSeries()
        self.series.setName('微信数据')
        self.line_chart.addSeries(self.series)

        # x = [i for i in range(len(self.data))]
        # for d, m in zip(self.data, x):
        #     self.series.append(m, d)

        for idx, value in enumerate(self.data):
            self.series.append(idx, value)

        axis_x = QBarCategoryAxis()
        axis_x.setCategories(self.attr.get('day'))
        axis_x.setTitleText('日')
        axis_y = QValueAxis()
        axis_y.setRange(0, 30)
        axis_y.setTitleText('元')

        self.line_chart.setAxisX(axis_x, self.series)
        self.line_chart.setAxisY(axis_y, self.series)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_data = [random.randint(15, 20) for _ in range(31)]
    test_attr = {
        'day': [(str(c+1)) for c in range(31)]

    }
    print(test_data)
    print(test_attr)
    my_line_chart = MoneyLineChart(test_data, test_attr)
    my_line_chart.show()
    sys.exit(app.exec_())


