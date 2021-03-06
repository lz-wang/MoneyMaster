#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: TimeFilter.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/6 下午11:26
import sys
import calendar
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QDateTime, QDate, QTime


INIT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')


class TimeFilterWidget(QWidget):
    def __init__(self,
                 start: datetime = INIT_DATETIME,
                 end: datetime = datetime.now(),
                 is_end_primary: bool = False):
        super().__init__()
        self.start = start
        self.end = end
        self.is_end_primary = is_end_primary
        self.__init_datetime()
        self.__init_ui()

    def __init_datetime(self):
        self.start_year = self.start.year
        self.start_month = self.start.month
        self.start_day = self.start.day

        self.end_year = self.end.year
        self.end_month = self.end.month
        self.end_day = self.end.day
        self.years = [y for y in range(self.start_year, self.end_year+1)]
        self.months = [m+1 for m in range(12)]
        self.days = [d+1 for d in range(31)]

    def __init_ui(self):
        # init year
        self.year_label = QLabel('Year: ')
        self.year_combox = QComboBox()
        for year in self.years:
            self.year_combox.addItem(str(year))
        if not self.is_end_primary:
            self.year_combox.setCurrentIndex(0)
        else:
            self.year_combox.setCurrentIndex(self.end_year-self.start_year)
        self.year_combox.currentTextChanged.connect(self.change_month)

        # init month
        self.month_label = QLabel('Month: ')
        self.month_combox = QComboBox()
        for month in self.months:
            self.month_combox.addItem(str(month))
        if not self.is_end_primary:
            self.month_combox.setCurrentIndex(self.start_month-1)
        else:
            self.month_combox.setCurrentIndex(self.end_month-1)
        self.month_combox.currentTextChanged.connect(self.change_day)

        # init day
        self.day_label = QLabel('Day: ')
        self.day_combox = QComboBox()
        for day in self.days:
            self.day_combox.addItem(str(day))
        if not self.is_end_primary:
            self.day_combox.setCurrentIndex(self.start_day-1)
        else:
            self.day_combox.setCurrentIndex(self.end_day-1)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.addWidget(self.year_label, 1, 1)
        self.grid.addWidget(self.year_combox, 1, 2)
        self.grid.addWidget(self.month_label, 2, 1)
        self.grid.addWidget(self.month_combox, 2, 2)
        self.grid.addWidget(self.day_label, 3, 1)
        self.grid.addWidget(self.day_combox, 3, 2)

        self.setLayout(self.grid)
        self.change_month()
        self.change_day()

    def change_month(self):
        year = int(str(self.year_combox.currentText()))
        month = int(str(self.month_combox.currentText()))

        if year == self.end_year:
            months = [m+1 for m in range(0, self.end_month)]
            month_value = self.end_month if month > self.end_month else month
        elif year == self.start_year:
            months = [m+1 for m in range(self.start_month-1, 12)]
            month_value = self.start_month if month < self.start_month else month
        else:
            months = self.months
            month_value = month
        self.month_combox.clear()
        for _month in months:
            self.month_combox.addItem(str(_month))
        self.month_combox.setCurrentText(str(month_value))

    def change_day(self):
        if self.month_combox.currentText() == '':
            return
        day = int(str(self.day_combox.currentText()))
        month = int(str(self.month_combox.currentText()))
        year = int(str(self.year_combox.currentText()))
        # print('%d-%d-%d' % (year, month, day))

        if month in [1, 3, 5, 7, 8, 10, 12]:
            day_max = 31
        elif month in [4, 6, 9, 11]:
            day_max = 30
        else:
            if calendar.isleap(year):
                day_max = 29
            else:
                day_max = 28
        if year == self.start_year and month == self.start_month:
            day_min = self.start_day
        elif year == self.end_year and month == self.end_month:
            day_min = 1
            day_max = self.end_day
        else:
            day_min = 1
        self.day_combox.clear()
        for _day in range(day_min-1, day_max):
            self.day_combox.addItem(str(_day + 1))
        day = day if day < day_max else day_max
        self.day_combox.setCurrentText(str(day))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # y = [x for x in range(2014, 2021)]
    # m = [x + 1 for x in range(12)]
    # d = [x + 1 for x in range(31)]
    ds = datetime.strptime('2015-07-25 00:00:00', '%Y-%m-%d %H:%M:%S')
    de = datetime.strptime('2019-06-20 00:00:00', '%Y-%m-%d %H:%M:%S')
    form = TimeFilterWidget(start=ds, end=de, is_end_primary=True)
    form.show()
    sys.exit(app.exec_())
