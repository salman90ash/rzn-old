# Generated by Django 4.1.1 on 2022-10-11 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TasksData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rzn_number', models.CharField(max_length=255, null=True, verbose_name='Вх. номер')),
                ('rzn_date', models.CharField(max_length=255, null=True, verbose_name='Вх. дата')),
                ('dec_number', models.CharField(max_length=255, null=True, verbose_name='Исх. номер')),
                ('dec_date', models.CharField(max_length=255, null=True, verbose_name='Исх. дата')),
                ('url', models.CharField(max_length=255, null=True, verbose_name='URL')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True, verbose_name='Завершено')),
                ('date_UPD', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='TasksNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активировать')),
            ],
        ),
        migrations.CreateModel(
            name='TasksType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активировать')),
            ],
        ),
        migrations.CreateModel(
            name='TasksKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.JSONField(blank=True, default={}, verbose_name='Ключ')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksdata')),
            ],
        ),
        migrations.AddField(
            model_name='tasksdata',
            name='notice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksnotice'),
        ),
        migrations.AddField(
            model_name='tasksdata',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rzn.taskstype'),
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rzn.tasksdata', verbose_name='Сведения')),
            ],
        ),
    ]
