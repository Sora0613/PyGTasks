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

        self.refresh()
        self.task_refresh()

        self.ui.pushButton_refresh.clicked.connect(self.refresh)
        self.ui.pushButton_add.clicked.connect(self.show_new_window)
        self.ui.pushButton_delete.clicked.connect(self.delete)
        self.ui.pushButton.clicked.connect(self.done)
        self.ui.comboBox_lists.currentIndexChanged.connect(self.task_refresh)

    def show_new_window(self, checked) :
        if self.w is None :
            self.w = Sub_Window()
            self.w.show()
        else :
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    ###タスク系の処理###

    def refresh(self) :  # リストの取得を行う
        self.ui.comboBox_lists.clear()
        creds = gt.authorize()
        list_names = gt.get_list(creds)
        self.ui.comboBox_lists.addItems(list_names.keys())

    def task_refresh(self) :  # タスクの取得を行う
        creds = gt.authorize()
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(creds)
        list_id_selected = list_names.get(tasklist_selected)
        if list_id_selected != None :
            self.ui.listWidget.clear()
            items = gt.get_tasks_in_tasklist(creds, list_id_selected)
            for item in items:
                self.ui.listWidget.addItem(item)


    def show_new_window(self, checked) :
        if self.w is None :
            self.w = Sub_Window()
            self.w.show()
        else :
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def delete(self) :  # listから選択しているものをgetして削除する
        creds = gt.authorize()
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(creds)
        list_id_selected = list_names.get(tasklist_selected)

        selected = self.ui.listWidget.currentItem().text()
        print(selected)

        tasks = gt.get_tasks_in_tasklist(creds, list_id_selected)
        selected_task_id = tasks.get(selected)

        gt.delete_task(creds, list_id_selected, selected_task_id)

        self.task_refresh()

        print("deleted.")

    def done(self) :
        creds = gt.authorize()
        tasklist_selected = self.ui.comboBox_lists.currentText()
        list_names = gt.get_list(creds)
        list_id_selected = list_names.get(tasklist_selected)

        selected = self.ui.listWidget.currentItem().text()
        print(selected)

        tasks = gt.get_tasks_in_tasklist(creds, list_id_selected)
        selected_task_id = tasks.get(selected)

        gt.done_task(creds, list_id_selected, selected, selected_task_id)

        self.task_refresh()


class Sub_Window(QDialog) :
    def __init__(self, parent=None) :
        super(Sub_Window, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.main = Main_Window()

        self.ui.pushButton.clicked.connect(self.add_task)

    def add_task(self) :
        title = self.ui.lineEdit.text()
        note = self.ui.lineEdit_2.text()

        creds = gt.authorize()
        tasklist_selected = (self.main.ui.comboBox_lists.currentText())
        list_id_selected = gt.get_list(creds).get(tasklist_selected)

        if title is None:
            print("title is None")
            return
        else:
            print("title : " + title)
            print("note : " + note)

            gt.add_task(creds, list_id_selected, title, note)  # タスクを追加
            print("task added")

            self.main.refresh()
            self.main.task_refresh()

            self.close()



if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
