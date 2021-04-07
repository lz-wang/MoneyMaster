#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MainWindow.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/7 下午9:53


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from utils.ConfigManager import ConfigTool
from ui.DatabaseView import DatabaseView
from ui.StatisticsView import StaticsView


class MoneyMainWindow(QMainWindow):

    def __init__(self):
        super(MoneyMainWindow, self).__init__()
        self.setWindowTitle('Money Master')
        self.__init_ui()
        self.__setup_ui()

    def _read_qss(self):
        ct = ConfigTool()
        cfg = ct.cfg_reader()
        list_style_qss = cfg['paths']['stylesheet']['SideBar']
        with open(list_style_qss, 'r') as f:
            self.list_style = f.read()

    def __init_ui(self):
        self._read_qss()

        self.left_widget = QListWidget()
        self.left_widget.setStyleSheet(self.list_style)
        self.right_widget = QStackedWidget()

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.resize(1200, 800)

    def __setup_ui(self):
        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定
        self.left_widget.setFrameShape(QListWidget.NoFrame)
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        label_items = ['HOME', 'DATABASE', 'STATICS', 'TODO']
        home_widget = QWidget()
        database_widget = DatabaseView()
        statics_widget = StaticsView()
        todo_widget = QWidget()
        content_items = [home_widget, database_widget, statics_widget, todo_widget]

        for label, content in zip(label_items, content_items):
            list_item = QListWidgetItem(label)
            list_item.setSizeHint(QSize(30, 60))
            list_item.setTextAlignment(Qt.AlignCenter)
            self.left_widget.addItem(list_item)

            self.right_widget.addWidget(content)

        self.left_widget.setCurrentRow(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = MoneyMainWindow()
    main_wnd.show()
    app.exec()
