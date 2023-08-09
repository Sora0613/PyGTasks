from __future__ import print_function

import os.path

#GUI関連
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTabWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QTextEdit, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

# ユーザー認証系
creds = None
if os.path.exists('token.json') :
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid :
    if creds and creds.expired and creds.refresh_token :
        creds.refresh(Request())
    else :
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token :
        token.write(creds.to_json())

#タスクの関数
def get_task_lists() :
    service = build('tasks', 'v1', credentials=creds)
    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items :
        print('No task lists found.')
        return

    return items

def add_task(tasklist, title, note) :
    service = build('tasks', 'v1', credentials=creds)
    task = {
        'title' : title,
        'notes' : note,
        'due' : ""
    }
    result = service.tasks().insert(tasklist=tasklist, body=task).execute() #tasklistはtasklistのid
    print(result)

def delete_task(tasklist, task) :
    service = build('tasks', 'v1', credentials=creds)
    result = service.tasks().delete(tasklist=tasklist, task=task).execute() #tasklist, taskはそれぞれのid
    print(result)


def main() :
    root = Tk()
    root.title("Google Tasks")
    root.geometry("500x500")

    options = {}

    items = get_task_lists()

    for item in items :
        options.setdefault(item['id'], item['title'])

    print(options)

    clicked = StringVar()
    clicked.set("")
    drop = OptionMenu(root, clicked, *options.values())
    drop.pack()

    root.mainloop()


if __name__ == '__main__' :
    main()
