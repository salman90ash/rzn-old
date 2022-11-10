from django.contrib import admin

from users.models import CustomUser


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('tg_chat_id', 'comments', 'tg_username', 'tg_first_name', 'tg_last_name')
#     list_display_links = ('tg_chat_id', 'comments', 'tg_username', 'tg_first_name', 'tg_last_name')
#     search_fields = ('tg_chat_id', 'comments', 'tg_username', 'tg_first_name', 'tg_last_name')
#
#
# admin.site.register(CustomUser, CustomUserAdmin)
