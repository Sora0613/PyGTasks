import os
import sys

import task_api

#GUI関連
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTabWidget, QApplication, QHBoxLayout, QVBoxLayout, \
    QLabel, QGridLayout, QLineEdit, QTextEdit, QDesktopWidget, QComboBox
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon
#from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        creds = task_api.authorize()

        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('sample')

        self.grid = QGridLayout()
        self.tasks_combo = QComboBox()
        self.task_lists_combo = QComboBox()
        self.button = QPushButton('get task list')
        self.task_add_button = QPushButton('add task')
        self.task_delete_button = QPushButton('delete task')
        self.label = QLabel('')

        self.tasks_combo.addItems(task_api.get_task_dict_values(creds))
        self.task_lists_combo.addItems(task_api.get_task_lists(creds))

        self.button.clicked.connect(lambda: self.label.setText(self.combo.currentText()))

        print(self.combo.currentText())

        # レイアウト配置
        self.grid.addWidget(self.button, 1, 0, 1, 1)
        self.grid.addWidget(self.label, 2, 0, 1, 2)
        self.grid.addWidget(self.tasks_combo, 0, 0, 1, 1)
        self.grid.addWidget(self.task_lists_combo, 3, 0, 1, 1)

        self.setLayout(self.grid)


        #
        self.show()

def main() :
    #creds = task_api.authorize()

    app = QApplication(sys.argv)
    main_window = MainWidget()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__' :
    main()
