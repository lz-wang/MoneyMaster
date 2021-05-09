#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: DatabaseUi.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/5/9 下午9:56

import os
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QMessageBox, QApplication, QLabel, QComboBox,
                             QFileDialog, QTableWidget, QTableWidgetItem, QDialog, QHBoxLayout, QVBoxLayout, QGridLayout)

from utils.LogManager import MoenyLogger
from utils.ConfigManager import ConfigTool
from utils.SQLiteManager import MySqlite
from utils.DataManager import DataManager


class DatabaseDialog(QDialog):
    def __init__(self):
        # data process
        super().__init__()
        self.log = MoenyLogger().logger
        self.cfg = ConfigTool().cfg_reader()
        self.db_path = self.cfg['paths']['database']['main']
        self.db = MySqlite(self.db_path)
        self.data_handler = DataManager()
        self.data_type = ''
        self.data = []
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle('数据库管理器')
        self.setFixedSize(900, 600)
        # TODO: 与通用的表格视图合并，弹出独立对话框形式
        self.table_show_data = QTableWidget()
        self.data_type_label = QLabel('数据类型')
        self.data_type_combobox = QComboBox()
        self.data_type_combobox.addItem('微信')
        self.data_type_combobox.addItem('支付宝')
        self.data_file_path = QLabel('文件路径')

        self._init_buttons()
        self._init_edits()
        self._init_layouts()

    def _init_buttons(self):
        # Push Button
        self.btn_import_file_data = QPushButton('导入单个文件')
        self.btn_batch_import_file_data = QPushButton('批量导入文件')
        self.btn_read_file_data = QPushButton('读取文件')
        self.btn_write_db = QPushButton('写入数据库')
        self.btn_reset_db = QPushButton('重置数据库')
        # 导入数据文件按钮
        self.btn_import_file_data.setToolTip('从文件中导入数据')
        self.btn_import_file_data.clicked.connect(self.import_data_file)
        self.btn_batch_import_file_data.clicked.connect(lambda: self.import_data_file(batch=True))
        # 读取数据按钮
        self.btn_read_file_data.clicked.connect(self.read_file_data)
        # 操作数据库按钮
        self.btn_write_db.setToolTip('必须先读取文件才能写入数据库')
        self.btn_write_db.clicked.connect(self.write_db)
        self.btn_write_db.setEnabled(False)
        self.btn_reset_db.clicked.connect(self.reset_db)
        
    def _init_edits(self):
        # LineEdit
        self.ledit_path = QLineEdit()
        self.ledit_path.setPlaceholderText('请选择或输入要导入的数据文件路径')
        
        # TextEdit
        self.tedit_review = QTextEdit()
        self.tedit_review.setTextColor(QColor('#2c387e'))
        self.tedit_review.setPlaceholderText('此处将显示导入的数据概览')
        self.tedit_review.setEnabled(False)
        
    def _init_layouts(self):
        # right: push buttons
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.btn_import_file_data)
        btn_layout.addWidget(self.btn_batch_import_file_data)
        btn_layout.addWidget(self.btn_read_file_data)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_write_db)
        btn_layout.addWidget(self.btn_reset_db)
        
        # left: line edit, text edit and data table
        edit_layout = QGridLayout()
        # gridlayout.addLayout(widget)
        # gridlayout.addLayout(widget, row, column)
        # gridlayout.addLayout(widget, row, column, rowspan, columnspan, alignment)
        edit_layout.addWidget(self.data_type_label, 1, 1)
        edit_layout.addWidget(self.data_type_combobox, 1, 2)
        edit_layout.addWidget(self.data_file_path, 1, 3)
        edit_layout.addWidget(self.ledit_path, 1, 4)
        edit_layout.addWidget(self.tedit_review, 2, 1, 4, 4)
        edit_layout.addWidget(self.table_show_data, 3, 1, 5, 4)

        # global layout
        global_layout = QHBoxLayout()
        global_layout.setContentsMargins(1, 0, 1, 0)
        global_layout.addLayout(edit_layout)
        global_layout.addLayout(btn_layout)
        self.setLayout(global_layout)

    def set_data_review(self, data: dict):
        review = '---------Data Review:---------\n'
        for k, v in data.items():
            item = k + ' --> ' + v + '\n'
            review += item
        self.tedit_review.setText(review)

    def set_tablewidget(self, data):
        self.table_show_data.clear()
        self.table_show_data.setColumnCount(len(data[0]))
        self.table_show_data.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
                self.table_show_data.setItem(i, j, item)

    def import_data_file(self, batch=False):
        dlg_open_files = QFileDialog()
        current_ledit_path = self.ledit_path.text()
        if os.path.exists(current_ledit_path):
            default_path = current_ledit_path
        else:
            default_path = os.environ['HOME']
        if batch is True:
            file_names = dlg_open_files.getOpenFileNames(self, directory=default_path)[0]
            file_name = '|'.join(file_names)
        else:
            file_name = dlg_open_files.getOpenFileName(self, directory=default_path)[0]
        if file_name:
            self.ledit_path.setText(file_name)

    def read_file_data(self):
        data_files_text = self.ledit_path.text()
        data_files_list = data_files_text.split('|')
        data_type = str(self.data_type_combobox.currentText())

        self.data.clear()
        all_review = {}
        for data_file in data_files_list:
            if not self.file_checker(data_file):
                return

            try:
                data, review = self.data_handler.read_data(data_type, data_file)
                self.data.extend(data)
                all_review.update(review)
            except Exception as e:
                QMessageBox.critical(self, '错误', '{}'.format(e), QMessageBox.Ok)
                return

        self.set_data_review(all_review)
        self.set_tablewidget(self.data)
        if not self.btn_write_db.isEnabled():
            self.btn_write_db.setEnabled(True)
            self.tedit_review.setEnabled(True)

    def write_db(self):
        self.log.info('----TO DB-----')
        self.data_type = self.data_type_combobox.currentText()
        print(self.data_type)
        self.data_handler.write_data_to_db(self.data, self.data_type)
        if not self.btn_reset_db.isEnabled():
            self.btn_reset_db.setEnabled(True)

    def reset_db(self):
        warning_msg = '重置数据库？\n\n此操作将导致您的数据全部丢失且无法恢复！'
        reply = QMessageBox.warning(self, '警告', warning_msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log.warning('--- CLEAR DB DATA ---')
            self.data_handler.reset_databse()

    def reset(self):
        self.tedit_review.clear()
        self.table_show_data.clear()
        self.btn_write_db.setEnabled(False)

    def file_checker(self, file_name):
        if file_name == '':
            QMessageBox.warning(self, '警告', '请选择文件', QMessageBox.Ok)
            return False
        if not os.path.exists(file_name):
            QMessageBox.warning(self, '警告', '所选文件不存在', QMessageBox.Ok)
            return False
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = DatabaseDialog()
    mm.show()
    sys.exit(app.exec_())
