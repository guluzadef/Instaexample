# Generated by Django 2.2.3 on 2019-08-31 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0053_auto_20190831_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='descmail',
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='descphone',
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='iconmail',
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='iconphone',
        ),
    ]
