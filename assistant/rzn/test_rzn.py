from rzn.models import Tasks, TasksKey, TasksData, TasksType, TasksNotice
from users.models import CustomUser
from users.models import CustomUser
from django.db import transaction
from rzn.actions import *
import json

tasks = TasksData.objects.filter(notice_id__gte=2)
list_result = []
for task in tasks:
    tasks_title = Tasks.objects.filter(data=2)
    for task_title in tasks_title:
        notice_text = task.notice.title
        user_tg_chat_id = task_title.user.tg_chat_id
        title = task_title.title
        url = task.url
        dict_result = {
            'chat_id': user_tg_chat_id,
            'title': title,
            'notice': notice_text,
            'url': url
        }
        list_result.append(dict_result)


print(json.dumps(list_result))
