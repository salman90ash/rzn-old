import json
import pprint

import rzn.actions as actions
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from rzn.models import TasksKey, TasksNotice, TasksType, TasksData, Tasks
from users.models import CustomUser
from django.core import serializers


# Create your views here.
@csrf_exempt
def tg_users(request):
    try:
        users = CustomUser.objects.values()
        # print(users)
        # result = json.dumps(users)
        return HttpResponse(users, content_type="application/json")
    except ObjectDoesNotExist:
        return HttpResponse(False)


@csrf_exempt
def tg_get_user(request, tg_chat_id):
    try:
        user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
        user_dict = {
            "id": user.id,
            "tg_chat_id": user.tg_chat_id,
            "task_title_detail": user.task_title_detail
        }
        return HttpResponse(json.dumps(user_dict), content_type="application/json")
    except ObjectDoesNotExist:
        return HttpResponse(False)


@csrf_exempt
def tg_create_user(request):
    # mydata = json.loads(request.body)
    # print(mydata)
    tg_chat_id = request.POST.get("tg_chat_id")
    tg_username = request.POST.get("tg_username")
    tg_first_name = request.POST.get("tg_first_name")
    tg_last_name = request.POST.get("tg_last_name")
    # print('BODY', request.body)
    username = 'username_' + str(tg_chat_id)
    user = CustomUser(username=username, tg_chat_id=tg_chat_id)
    if tg_username:
        user.tg_username = tg_username

    if tg_first_name:
        user.tg_first_name = tg_first_name

    if tg_last_name:
        user.tg_last_name = tg_last_name

    try:
        user.save()
        return HttpResponse(user)
    except IntegrityError:
        return HttpResponse(False)


@csrf_exempt
@transaction.atomic
def tg_create_task(request):
    tg_chat_id = request.POST.get("tg_chat_id")
    type_id = int(request.POST.get("type"))
    title = request.POST.get("name_md")
    number = request.POST.get("number")
    date = request.POST.get("date")

    if type_id == 6:  # если по исх.
        data = TasksData.objects.filter(type_id=type_id, dec_number=number, dec_date=date)
    else:  # если по вх.
        data = TasksData.objects.filter(type_id=type_id, rzn_number=number, rzn_date=date)

    if data.count() == 1:
        data = data[0]
    else:
        url = actions.set_url(number, date, type_id)
        notice = TasksNotice.objects.get(id=1)

        if type_id == 6:  # если по исх.
            type = TasksType.objects.get(id=type_id)
            data = TasksData(dec_number=number,
                             dec_date=date,
                             url=url,
                             # key=key,
                             notice=notice,
                             type=type
                             )
            data.save()
        else:  # если по вх.
            type = TasksType.objects.get(id=type_id)
            data = TasksData(rzn_number=number,
                             rzn_date=date,
                             url=url,
                             # key=key,
                             notice=notice,
                             type=type
                             )
            data.save()

        key_value = actions.get_key(type_id=type_id, number=number, date=date)
        key = TasksKey(value=key_value,
                       data=data
                       )
        key.save()

    user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
    task = Tasks(title=title,
                 user=user,
                 data=data)
    task.save()
    return HttpResponse(task)


@csrf_exempt
@transaction.atomic
def tg_send_updates(request):
    tasks = TasksData.objects.filter(notice_id__gte=2)
    list_result = []
    for task in tasks:
        tasks_title = Tasks.objects.filter(data=task.pk, is_active=True)
        for task_title in tasks_title:
            notice_text = task.notice.title
            user_tg_chat_id = task_title.user.tg_chat_id
            title = task_title.title
            task_type = task.type.title
            completed = task.completed
            url = task.url
            dict_result = {
                'chat_id': user_tg_chat_id,
                'taskdata_id': task.id,
                'type': task_type,
                'title': title,
                'notice': notice_text,
                'completed': completed,
                'url': url
            }
            list_result.append(dict_result)
    result = json.dumps(list_result)
    return HttpResponse(result, content_type="application/json")


def set_task_info(task, title_details=True):
    title = ''
    if task.data.type.id == 6:
        title = actions.get_title_task_details(task.title, task.data.type.id, task.data.type.title,
                                               task.data.dec_number, task.data.dec_date)
    else:
        title = actions.get_title_task_details(task.title, task.data.type.id, task.data.type.title,
                                               task.data.rzn_number, task.data.rzn_date)
    if title_details:
        return {
            'id': task.id,
            'title': title,
            'url': task.data.url
        }
    return {
        'id': task.id,
        'title': f"{task.title} ({task.data.type.title})",
        'url': task.data.url
    }


@csrf_exempt
@transaction.atomic
def tg_list_tasks(request, tg_chat_id):
    user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
    tasks = Tasks.objects.filter(user=user.id, is_active=True)
    list_result = []
    title_details = user.task_title_detail
    if title_details:
        for task in tasks:
            list_result.append(set_task_info(task))
    else:
        for task in tasks:
            list_result.append(set_task_info(task, False))
    result = json.dumps(list_result)
    return HttpResponse(result, content_type="application/json")


@csrf_exempt
def tg_del_task(request, task_id):
    try:
        task = Tasks.objects.get(id=task_id)
        task.is_active = False
        task.save()
        result_dict = {
            "title": task.title,
            "type_id": task.data.type.id,
            "type_title": task.data.type.title,
        }
        if actions.check_rzn_details(task.data.type.id):
            result_dict['number'] = task.data.rzn_number
            result_dict['date'] = task.data.rzn_date
        else:
            result_dict['number'] = task.data.dec_number
            result_dict['date'] = task.data.dec_date
        result = json.dumps(result_dict)
        return HttpResponse(result, content_type="application/json")
    except ObjectDoesNotExist:
        return HttpResponse(False)


@csrf_exempt
def tg_update_tasks(request):
    # print('start update_tasks')
    actions.update_tasks()
    result = json.dumps({'answer': 'ok'})
    return HttpResponse(result, content_type="application/json")



@csrf_exempt
def tg_change_notice_1(request, taskdata_id):
    task = TasksData.objects.get(id=taskdata_id)
    notice = TasksNotice.objects.get(pk=1)
    task.notice = notice
    task.save()
    return HttpResponse(task, content_type="application/json")


@csrf_exempt
def tg_task_detail(request, tg_chat_id):
    if request.method == "GET":
        user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
        return HttpResponse(json.dumps({"task_title_detail": f"{user.task_title_detail}"}),
                            content_type="application/json")
    elif request.method == "POST":
        value = request.POST.get("task_title_detail")
        if value.lower() == "true":
            value = True
        else:
            value = False
        user = CustomUser.objects.get(tg_chat_id=tg_chat_id)
        user.task_title_detail = value
        user.save()
        return HttpResponse(json.dumps({"task_title_detail": f"{user.task_title_detail}"}),
                            content_type="application/json")

