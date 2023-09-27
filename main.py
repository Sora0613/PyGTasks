import sys

import PyGTasks as gt

# GUI関連
from PyQt5.QtWidgets import *

from Design.add_popup import Ui_Form
from Design.taskmanager import Ui_Main


class Main_Window(QDialog) :
    def __init__(self, parent=None) :
        super(Main_Window, self).__init__(parent)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.w = None
        self.creds = gt.authorize()

        self.refresh()
        self.task_refresh()

        self.ui.pushButton_refresh.clicked.connect(self.refresh)
        self.ui.pushButton_add.clicked.connect(self.show_new_window)
        self.ui.pushButton_delete.clicked.connect(self.delete)
        self.ui.pushButton.clicked.connect(self.done)
        self.ui.comboBox_lists.currentIndexChanged.connect(self.task_refresh)

    def show_new_window(self) :
        if self.w is None :
            self.w = Sub_Window()
            self.w.show()
        else :
            self.w.close()
            self.w = None

    ###タスク系の処理###

    def refresh(self) :  # リストの取得を行う
        self.ui.comboBox_lists.clear()
        list_names = gt.get_list(self.creds)
        self.ui.comboBox_lists.addItems(list_names.keys())

    def task_refresh(self) :  # タスクの取得を行う
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(self.creds)
        list_id_selected = list_names.get(tasklist_selected)
        if list_id_selected is not None :
            self.ui.listWidget.clear()
            items = gt.get_tasks_in_tasklist(self.creds, list_id_selected)
            for item in items :
                self.ui.listWidget.addItem(item)

    def delete(self) :  # listから選択しているものをgetして削除する
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(self.creds)
        list_id_selected = list_names.get(tasklist_selected)

        selected = self.ui.listWidget.currentItem().text()

        tasks = gt.get_tasks_in_tasklist(self.creds, list_id_selected)
        selected_task_id = tasks.get(selected)

        gt.delete_task(self.creds, list_id_selected, selected_task_id)

        self.task_refresh()

    def done(self) :
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(self.creds)
        list_id_selected = list_names.get(tasklist_selected)

        tasks = gt.get_tasks_in_tasklist(self.creds, list_id_selected)

        if self.ui.listWidget.currentItem() is not None :
            selected_task_id = tasks.get(self.ui.listWidget.currentItem().text())

            gt.done_task(self.creds, list_id_selected, selected_task_id)

            self.task_refresh()


class Sub_Window(QDialog) :
    def __init__(self, parent=None) :
        super(Sub_Window, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.creds = gt.authorize()

        self.main = Main_Window()

        self.ui.pushButton.clicked.connect(self.add_task)

    def add_task(self) :
        title = self.ui.lineEdit.text()
        note = self.ui.lineEdit_2.text()

        tasklist_selected = (self.main.ui.comboBox_lists.currentText())
        list_id_selected = gt.get_list(self.creds).get(tasklist_selected)

        if title is not None :
            gt.add_task(self.creds, list_id_selected, title, note)  # タスクを追加
            self.main.task_refresh()
            self.close()



if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
