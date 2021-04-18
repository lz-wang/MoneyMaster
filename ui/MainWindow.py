#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: MainWindow.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/19 上午12:32


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from utils.ConfigManager import ConfigTool
from ui.DatabaseView import DatabaseView
from ui.StatisticsView import StaticsView
from ui.DatabaseUi import DatabaseDlg
from ui.TodoDialog import show_todo


class MoneyMainWindow(QMainWindow):

    def __init__(self):
        super(MoneyMainWindow, self).__init__()
        self.setWindowTitle('Money Master')
        self.__init_ui()
        self.__setup_ui()

    def _read_qss(self):
        ct = ConfigTool()
        self.cfg = ct.cfg_reader()
        self.list_style_qss = self.cfg['paths']['stylesheet']['SideBar']
        with open(self.list_style_qss, 'r') as f:
            self.list_style = f.read()
        self.icons = self.cfg['paths']['icons']
        self.icon_btn_style_qss = self.cfg['paths']['stylesheet']['IconButton']
        with open(self.icon_btn_style_qss, 'r') as f:
            self.icon_btn_style = f.read()

    def __init_ui(self):
        self._read_qss()

        self.func_list = QListWidget()
        self.icon_area = QWidget()
        self.setting_dlg = DatabaseDlg()
        self.setting_dlg.setWindowModality(Qt.ApplicationModal)
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.func_list)
        self.left_layout.addWidget(self.icon_area)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_widget = QListWidget()
        self.left_widget.setStyleSheet(self.list_style)
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setFrameShape(QFrame.NoFrame)
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
        self.__set_up_functions()
        self.__set_up_icons()

    def __set_up_functions(self):
        self.func_list.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定
        self.func_list.setFrameShape(QListWidget.NoFrame)
        self.func_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.func_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
            self.func_list.addItem(list_item)

            self.right_widget.addWidget(content)

        self.func_list.setCurrentRow(0)

    def __set_up_icons(self):
        self.btn_setting = QPushButton()
        self.btn_setting.setIcon(QIcon(self.icons['setting']))
        self.btn_setting.clicked.connect(self.show_setting)

        self.btn_help = QPushButton()
        self.btn_help.setIcon(QIcon(self.icons['help']))
        self.btn_help.clicked.connect(self.show_help)

        icon_layout = QVBoxLayout()
        icon_layout.addWidget(self.btn_setting)
        icon_layout.addWidget(self.btn_help)
        self.icon_area.setLayout(icon_layout)
        self.icon_area.setStyleSheet(self.icon_btn_style)

    def show_setting(self):
        self.setting_dlg.show()
        self.setting_dlg.reset()

    def show_help(self):
        show_todo(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = MoneyMainWindow()
    main_wnd.show()
    app.exec()
