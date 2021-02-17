import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QTextEdit,
                             QGridLayout, QApplication, QLabel, QSlider,
                             QMessageBox, QFileDialog)


class MMGui(QWidget):
    def __init__(self):
        super().__init__()

        # Push Button
        self.btn_import = QPushButton()
        self.btn_read = QPushButton()
        self.btn_update = QPushButton()

        # LineEdit
        self.ledit_path = QLineEdit()

        # TextEdit
        self.tedit_data = QTextEdit()
        self.tedit_debug_console = QTextEdit()

        # Layout
        self.grid = QGridLayout()

        self.init_gui()
        
    def init_gui(self):
        self.init_pushbutton()
        self.init_lineedit()
        self.init_textedit()
        self.init_layout()
        self.init_window()

        self.show()

    def init_pushbutton(self):
        # 导入数据文件按钮
        self.btn_import.setText('导入数据')
        self.btn_import.setToolTip('Import WechatPay or Alipay data')
        self.btn_import.clicked.connect(self.import_data_file)

        # 读取数据按钮
        self.btn_read.setText('读取数据')
        self.btn_read.clicked.connect(self.read_data)

    def init_lineedit(self):
        pass

    def init_textedit(self):
        self.tedit_data.setTextColor(QColor('#2c387e'))

    def init_layout(self):
        # 设置组件布局
        self.grid.setSpacing(10)
        self.grid.addWidget(self.ledit_path, 1, 0, 1, 4)
        self.grid.addWidget(self.btn_import, 1, 4)
        self.grid.addWidget(self.btn_read, 1, 5)
        self.grid.addWidget(self.tedit_data, 2, 0, 3, 6)
        # self.grid.addWidget(self.tedit_debug_console, 3, 0, 5, 6)
        self.setLayout(self.grid)

    def init_window(self):
        self.resize(600, 400)
        self.setWindowTitle('Money Master')

    def import_data_file(self):
        dialog = QFileDialog()
        f_name = dialog.getOpenFileName(self, 'CHOOSE DATA', 'Python (*.py)')
        print(f_name[0])
        self.ledit_path.setText(f_name[0])

    def read_data(self):
        file_name = self.ledit_path.text()
        # self.console_info('file name: ' + file_name)
        with open(file_name) as f:
            data = f.read()
            self.tedit_data.setText(data)

    def console_info(self, text):
        print(text)
        self.tedit_debug_console.setTextColor(QColor(200, 0, 0))
        self.tedit_debug_console.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mm = MMGui()
    sys.exit(app.exec_())
