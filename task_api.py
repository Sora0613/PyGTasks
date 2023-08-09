from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

def authorize() :
    SCOPES = ['https://www.googleapis.com/auth/tasks']
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
    return creds

def get_task_lists(creds) :
    service = build('tasks', 'v1', credentials=creds)
    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items :
        print('No task lists found.')
        return

    return items

def add_task(creds, tasklist, title, note) :
    service = build('tasks', 'v1', credentials=creds)
    task = {
        'title' : title,
        'notes' : note,
        'due' : ""
    }
    result = service.tasks().insert(tasklist=tasklist, body=task).execute() #tasklistはtasklistのid
    print(result)

def delete_task(creds, tasklist, task) :
    service = build('tasks', 'v1', credentials=creds)
    result = service.tasks().delete(tasklist=tasklist, task=task).execute() #tasklist, taskはそれぞれのid
    print(result)

def get_task_dict_values(creds) :
    options = {}

    items = get_task_lists(creds)

    for item in items :
        options.setdefault(item['id'], item['title'])

    return options.values()

def get_task_dict_keys(creds) :
    options = {}

    items = get_task_lists(creds)

    for item in items :
        options.setdefault(item['id'], item['title'])

    return options.keys()

def get_tasks_in_tasklist(creds, tasklist) :
    service = build('tasks', 'v1', credentials=creds)
    tasks = service.tasks().list(tasklist=tasklist).execute()
    options = []
    #print(tasks)
    for task in tasks['items'] :
        if task['title'] :
            options.append(task['title'])
            print(task['title'])