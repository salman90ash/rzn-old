# Generated by Django 4.1.1 on 2022-12-18 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_task_title_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='type_sort',
            field=models.CharField(default='date_created_ASC', max_length=255, verbose_name='Telegram username'),
        ),
    ]
