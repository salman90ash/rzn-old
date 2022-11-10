from django.db import models
from assistant.settings import AUTH_USER_MODEL


# Create your models here.

class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    data = models.ForeignKey('TasksData', on_delete=models.CASCADE, verbose_name='Сведения')
    is_active = models.BooleanField(default=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title


class TasksType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    comment = models.CharField(max_length=255, verbose_name='Комментарии', default='')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активировать')

    def __str__(self):
        return self.title


class TasksNotice(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='Активировать')

    def __str__(self):
        return self.title


class TasksData(models.Model):
    rzn_number = models.CharField(max_length=255, verbose_name='Вх. номер', null=True)
    rzn_date = models.CharField(max_length=255, verbose_name='Вх. дата', null=True)
    dec_number = models.CharField(max_length=255, verbose_name='Исх. номер', null=True)
    dec_date = models.CharField(max_length=255, verbose_name='Исх. дата', null=True)
    url = models.CharField(max_length=255, verbose_name='URL', null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    completed = models.BooleanField(default=False, blank=True, verbose_name='Завершено', null=True)
    date_UPD = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True)
    # key = models.ForeignKey('TasksKey', on_delete=models.CASCADE, null=True)
    notice = models.ForeignKey('TasksNotice', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey('TasksType', on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    def __str__(self):
        res = f"type={self.type.title}"
        if self.rzn_number is not None:
            res = res + f" number={self.rzn_number}"
        if self.rzn_date is not None:
            res = res + f" date={self.rzn_date}"
        if self.dec_number is not None:
            res = res + f" dec_number={self.dec_number}"
        if self.dec_date is not None:
            res = res + f" dec_date={self.dec_date}"
        return res


class TasksKey(models.Model):
    value = models.JSONField(default={}, blank=True, verbose_name='Ключ')
    date_create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    data = models.ForeignKey('TasksData', on_delete=models.CASCADE, null=True)

    def compare(self, other):
        if self.value == '':
            return 1  # Нет обновлений.
        else:
            if other.value == '':
                return 2  # Обновилась информация на сайте.
            else:
                if self == other:
                    for i in range(len(self.value)):
                        if self.value[i] != other.value[i]:
                            return 2  # Обновилась информация на сайте.
                        # print(f"{self.value[i]} == {other.value[i]}")
                elif self > other:
                    return 3  # Увеличилось количество строк на сайте.
                elif self < other:
                    return 4  # Уменьшилось количество строк.
        return 1

    def __eq__(self, other):
        return len(self.value) == len(other.value)

    def __lt__(self, other):
        return len(self.value) < len(other.value)

    def __gt__(self, other):
        return len(self.value) > len(other.value)


