"""assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'tasks', TaskViewSet)
from tg_bot.views import tg_create_user, tg_create_task, tg_get_user, tg_send_updates, tg_list_tasks, tg_del_task,\
    tg_update_tasks, tg_change_notice_1, tg_users, tg_task_detail, tg_get_sort_info, tg_set_type_sort, tg_test

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),
    path('tg/api/v1/<str:token>/create_user/', tg_create_user),
    path('tg/api/v1/<str:token>/users/', tg_users),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/', tg_get_user),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/getSortInfo/', tg_get_sort_info),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/setSort/', tg_set_type_sort),
    path('tg/api/v1/<str:token>/users/<int:tg_chat_id>/task_detail/', tg_task_detail),
    path('tg/api/v1/<str:token>/create_task/', tg_create_task),
    path('tg/api/v1/<str:token>/tg_send_updates/', tg_send_updates),
    path('tg/api/v1/<str:token>/list_tasks/<int:tg_chat_id>/', tg_list_tasks),
    path('tg/api/v1/<str:token>/del_tasks/<int:task_id>/', tg_del_task),
    path('tg/api/v1/<str:token>/update_tasks/', tg_update_tasks),
    path('tg/api/v1/<str:token>/tg_change_notice_1/<int:taskdata_id>/', tg_change_notice_1),
    path('tg/api/v1/<str:token>/tg_test/', tg_test)
]
