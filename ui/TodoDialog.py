#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: TodoDialog.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/19 上午12:32

from PyQt5.QtWidgets import QMessageBox


def show_todo(self):
    QMessageBox.information(self, "提示", "此功能正在开发中", QMessageBox.Yes)
