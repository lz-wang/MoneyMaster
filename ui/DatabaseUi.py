#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DatabaseUi.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/19 上午12:32

import os
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QMessageBox, QApplication,
                             QFileDialog, QTableWidget, QTableWidgetItem, QDialog, QHBoxLayout, QVBoxLayout)

from utils.WechatPayManager import DataManager
from utils.LogManager import MoenyLogger
from utils.ConfigManager import ConfigTool
from utils.SQLiteManager import MySqlite


class DatabaseDlg(QDialog):
    def __init__(self):
        # data process
        super().__init__()
        self.wechat = DataManager()
        self.log = MoenyLogger().logger
        self.cfg = ConfigTool().cfg_reader()
        self.db_path = self.cfg['paths']['database']['main']
        self.db = MySqlite(self.db_path)

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
        self.global_layout = QHBoxLayout()
        self.global_layout.setContentsMargins(1, 0, 1, 0)
        self.edit_layout = QVBoxLayout()
        self.btn_layout = QVBoxLayout()

        self.init_gui()
        
    def init_gui(self):
        self.init_pushbutton()
        self.init_lineedit()
        self.init_textedit()
        self.init_tablewidget()
        self.init_layout()
        self.init_window()

    def init_pushbutton(self):
        # 导入数据文件按钮
        self.btn_import_file_data.setText('导入文件')
        self.btn_import_file_data.setToolTip('从文件中导入数据')
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
        self.ledit_path.setPlaceholderText('请选择或输入要导入的数据文件路径')

    def init_textedit(self):
        self.tedit_review.setTextColor(QColor('#2c387e'))
        self.tedit_review.setPlaceholderText('此处显示导入的数据概览')
        self.tedit_review.setEnabled(False)

    def set_data_review(self, data: dict):
        review = '---------Data Review:---------\n'
        for k, v in data.items():
            item = k + ' --> ' + v + '\n'
            review += item
        self.tedit_review.setText(review)

    def init_tablewidget(self):
        pass

    def set_tablewidget(self, data):
        self.table_show_data.clear()
        self.table_show_data.setColumnCount(len(data[0]))
        self.table_show_data.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
                self.table_show_data.setItem(i, j, item)

    def init_layout(self):
        # 设置组件布局
        self.edit_layout.addWidget(self.ledit_path)
        self.edit_layout.addWidget(self.tedit_review)
        self.edit_layout.addWidget(self.table_show_data)

        self.btn_layout.addWidget(self.btn_import_file_data)
        self.btn_layout.addWidget(self.btn_read_file_data)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_read_db)
        self.btn_layout.addWidget(self.btn_write_db)
        self.btn_layout.addWidget(self.btn_clear_db)

        self.global_layout.addLayout(self.edit_layout)
        self.global_layout.addLayout(self.btn_layout)
        self.setLayout(self.global_layout)

    def init_window(self):
        self.setFixedSize(800, 500)
        self.setWindowTitle('数据库管理器')

    def import_data_file(self):
        dialog = QFileDialog()
        current_ledit_path = self.ledit_path.text()
        if os.path.exists(current_ledit_path):
            default_path = current_ledit_path
        else:
            default_path = os.environ['HOME']
        # 选择一组文件导入
        file_names = dialog.getOpenFileNames(self, caption='CHOOSE DATA', directory=default_path)[0]
        f_name_text = '|'.join(file_names)
        if file_names:
            self.ledit_path.setText(f_name_text)

    def read_file_data(self):
        file_name = self.ledit_path.text()
        self.wechat.read_csv_data(file_name)
        self.set_data_review(self.wechat.wechat_data.statistics)
        self.set_tablewidget(self.wechat.wechat_data.data)
        if not self.btn_write_db.isEnabled():
            self.btn_write_db.setEnabled(True)
            self.tedit_review.setEnabled(True)

    def read_db(self):
        data = self.wechat.db.query_all_data(self.wechat.wechat_db.table_name)
        self.set_tablewidget(data)

    def write_db(self):
        self.log.info('----TO DB-----')
        self.wechat.write_data_to_db(data=self.wechat.wechat_data.data)
        if not self.btn_clear_db.isEnabled():
            self.btn_clear_db.setEnabled(True)

    def clear_db(self):
        warning_msg = '清空数据库？\n\n此操作将导致您的数据全部丢失且无法恢复！'
        reply = QMessageBox.warning(self, '警告', warning_msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log.warning('--- CLEAR DB DATA ---')
            self.db.delete_db()

    def reset(self):
        self.tedit_review.clear()
        self.table_show_data.clear()
        self.btn_write_db.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = DatabaseDlg()
    mm.show()
    sys.exit(app.exec_())
