#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: TestUi.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/3 下午11:25

import os
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QTextEdit, QMessageBox, QMainWindow,
                             QGridLayout, QApplication, QFileDialog, QTableWidget, QTableWidgetItem)

from WechatPay.WechatPayManager import DataManager


class MMGui(QWidget):
    def __init__(self):
        # data process
        super().__init__()
        self.wechat = DataManager()
        self.log = self.wechat.log

        # Push Button
        self.btn_import_file_data = QPushButton()
        self.btn_read_file_data = QPushButton()
        self.btn_read_db = QPushButton()
        self.btn_write_db = QPushButton()
        self.btn_clear_db = QPushButton()
        self.btn_update = QPushButton()

        # LineEdit
        self.ledit_path = QLineEdit()

        # TextEdit
        self.tedit_review = QTextEdit()

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

    def init_lineedit(self):
        data_path = os.getcwd() + '/data'
        wechat_demo = data_path + '/wechat/微信支付账单(20201001-20201231).csv'
        self.ledit_path.setText(wechat_demo)

    def init_textedit(self):
        self.tedit_review.setTextColor(QColor('#2c387e'))

    def set_data_review(self, data: dict):
        review = '---------Data Review:---------\n'
        for k, v in data.items():
            item = k + ' --> ' + v + '\n'
            review += item
        self.tedit_review.setText(review)

    def init_tablewidget(self):
        # self.table_show_data.setVisible(False)
        pass

    def set_tablewidget(self, data):
        self.table_show_data.clear()
        self.table_show_data.setColumnCount(len(data[0]))
        self.table_show_data.setRowCount(len(data))
        # self.table_show_data.setHorizontalHeaderLabels(self.wechat.csv_head)
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
                self.table_show_data.setItem(i, j, item)

    def init_layout(self):
        # 设置组件布局
        self.grid.setSpacing(10)
        self.grid.addWidget(self.ledit_path, 1, 0, 1, 6)
        self.grid.addWidget(self.btn_import_file_data, 1, 7)
        self.grid.addWidget(self.btn_read_file_data, 1, 8)
        self.grid.addWidget(self.btn_read_db, 2, 7)
        self.grid.addWidget(self.btn_write_db, 2, 8)
        self.grid.addWidget(self.btn_clear_db, 3, 8)
        self.grid.addWidget(self.tedit_review, 2, 0, 5, 6)
        self.grid.addWidget(self.table_show_data, 5, 0, 6, 6)
        self.setLayout(self.grid)

    def init_window(self):
        self.resize(1200, 1000)
        self.setWindowTitle('Money Master')

    def import_data_file(self):
        dialog = QFileDialog()
        f_name = dialog.getOpenFileNames(self, caption='CHOOSE DATA',
                                         directory='/Users/lzwang/PyProjects/MoneyMaster/data/wechat/')[0]
        f_name_text = '|'.join(f_name)
        if f_name:
            self.ledit_path.setText(f_name_text)

    def read_file_data(self):
        file_name = self.ledit_path.text()
        # self.console_info('file name: ' + file_name)
        self.wechat.read_csv_data(file_name)
        self.set_data_review(self.wechat.wechat_data.statistics)
        self.set_tablewidget(self.wechat.wechat_data.data)
        if not self.btn_write_db.isEnabled():
            self.btn_write_db.setEnabled(True)

    def read_db(self):
        data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        self.set_tablewidget(data)

    def write_db(self):
        self.log.info('----TO DB-----')
        self.wechat.write_data_to_db(data=self.wechat.wechat_data.data)
        if not self.btn_clear_db.isEnabled():
            self.btn_clear_db.setEnabled(True)

    def clear_db(self):
        reply = QMessageBox.warning(self, '警告', '清空数据库？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log.warning('--- CLEAR DB DATA ---')
            self.wechat.clear_db_data()

    def console_info(self, text):
        print(text)
        self.tedit_debug_console.setTextColor(QColor(200, 0, 0))
        self.tedit_debug_console.setText(text)


def run_gui():
    app = QApplication(sys.argv)
    mm = MMGui()
    sys.exit(app.exec_())
