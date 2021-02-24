#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: main_gui.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/2/24 下午9:33

import os
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QTextEdit,
                             QGridLayout, QApplication, QFileDialog, QTableWidget, QTableWidgetItem)

from WechatPay.WechatPayManager import DataManager


class MMGui(QWidget):
    def __init__(self):
        super().__init__()
        # data process
        self.wechat = DataManager()
        self.log = self.wechat.log

        # Push Button
        self.btn_import_file_data = QPushButton()
        self.btn_read_file_data = QPushButton()
        self.btn_read_db = QPushButton()
        self.btn_write_db = QPushButton()
        self.btn_clear_db = QPushButton()
        self.btn_update = QPushButton()
        self.btn_switch_view = QPushButton()

        # LineEdit
        self.ledit_path = QLineEdit()

        # TextEdit
        self.tedit_data = QTextEdit()
        self.tedit_review = QTextEdit()
        self.tedit_debug_console = QTextEdit()

        # TableWidget
        self.table_show_data = QTableWidget()

        # Layout
        self.grid = QGridLayout()

        self.init_gui()
        
    def init_gui(self):
        self.init_pushbutton()
        self.init_lineedit()
        self.init_textedit()
        self.init_tablewidget()
        self.init_layout()
        self.init_window()

        self.show()

    def init_pushbutton(self):
        # 导入数据文件按钮
        self.btn_import_file_data.setText('导入文件')
        self.btn_import_file_data.setToolTip('Import WechatPay or Alipay data')
        self.btn_import_file_data.clicked.connect(self.import_data_file)

        # 读取数据按钮
        self.btn_read_file_data.setText('读取文件')
        self.btn_read_file_data.clicked.connect(self.read_file_data)

        # 读写数据库
        self.btn_read_db.setText('读取数据库')
        self.btn_read_db.clicked.connect(self.read_db)

        self.btn_write_db.setText('写入数据库')
        self.btn_write_db.clicked.connect(self.write_db)
        self.btn_write_db.setEnabled(False)

        self.btn_clear_db.setText('清空数据库')
        self.btn_clear_db.clicked.connect(self.clear_db)
        self.btn_clear_db.setEnabled(False)

        # 切换textedit和table视图
        self.btn_switch_view.setText('切换视图')
        self.btn_switch_view.clicked.connect(self.switch_view)

    def init_lineedit(self):
        data_path = os.getcwd() + '/data'
        wechat_demo = data_path + '/wechat/wechat2020Q4.csv'
        self.ledit_path.setText(wechat_demo)

    def init_textedit(self):
        self.tedit_data.setTextColor(QColor('#2c387e'))

    def set_data_review(self, data: dict):
        review = '---------Data Review:---------\n'
        for k, v in data.items():
            item = k + ' --> ' + v + '\n'
            review += item
        self.tedit_review.setText(review)
        pass

    def init_tablewidget(self):
        # self.table_show_data.setVisible(False)
        pass

    def set_tablewidget(self, data):
        self.table_show_data.clear()
        self.table_show_data.setColumnCount(len(data[0]))
        self.table_show_data.setRowCount(len(data))
        self.table_show_data.setHorizontalHeaderLabels(data[0])
        for i in range(len(data)-1):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i+1][j]))
                self.table_show_data.setItem(i, j, item)
        print(len(data))
        print(len(data[0]))

    def init_layout(self):
        # 设置组件布局
        self.grid.setSpacing(10)
        self.grid.addWidget(self.ledit_path, 1, 0, 1, 6)
        self.grid.addWidget(self.btn_import_file_data, 1, 7)
        self.grid.addWidget(self.btn_read_file_data, 1, 8)
        self.grid.addWidget(self.btn_read_db, 2, 7)
        self.grid.addWidget(self.btn_write_db, 2, 8)
        self.grid.addWidget(self.btn_clear_db, 3, 8)
        # self.grid.addWidget(self.btn_switch_view, 3, 7)
        # self.grid.addWidget(self.tedit_data, 2, 0, 6, 6)
        self.grid.addWidget(self.tedit_review, 2, 0, 5, 6)
        self.grid.addWidget(self.table_show_data, 5, 0, 6, 6)
        # self.grid.addWidget(self.tedit_debug_console, 3, 0, 5, 6)
        self.setLayout(self.grid)

    def init_window(self):
        self.resize(1200, 1000)
        self.setWindowTitle('Money Master')

    def import_data_file(self):
        dialog = QFileDialog()
        f_name = dialog.getOpenFileName(self, 'CHOOSE DATA', 'Python (*.py)')
        print(f_name[0])
        if f_name[0] != '':
            self.ledit_path.setText(f_name[0])

    def read_file_data(self):
        file_name = self.ledit_path.text()
        # self.console_info('file name: ' + file_name)
        self.wechat.read_csv_data(file_name)
        self.set_data_review(self.wechat.wechat_data.statistics)
        self.set_tablewidget(self.wechat.wechat_data.data)
        with open(file_name) as f:
            data = f.read()
            self.tedit_data.setText(data)
        if not self.btn_write_db.isEnabled():
            self.btn_write_db.setEnabled(True)

    def read_db(self):
        pass

    def write_db(self):
        self.log.info('----TO DB-----')
        self.wechat.write_data_to_db(data=self.wechat.wechat_data.data)
        if not self.btn_clear_db.isEnabled():
            self.btn_clear_db.setEnabled(True)

    def clear_db(self):
        self.log.warning('--- CLEAR DB DATA ---')
        self.wechat.clear_db_data()

    def switch_view(self):
        if self.tedit_data.isVisible():
            self.tedit_data.setVisible(False)
            self.table_show_data.setVisible(True)
        else:
            self.tedit_data.setVisible(True)
            self.table_show_data.setVisible(False)

    def console_info(self, text):
        print(text)
        self.tedit_debug_console.setTextColor(QColor(200, 0, 0))
        self.tedit_debug_console.setText(text)


def run_gui():
    app = QApplication(sys.argv)
    mm = MMGui()
    sys.exit(app.exec_())
