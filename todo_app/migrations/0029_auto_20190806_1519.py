# Generated by Django 2.2.3 on 2019-08-06 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0028_postpage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostPage',
            new_name='Post',
        ),
    ]
