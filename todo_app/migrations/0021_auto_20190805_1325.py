# Generated by Django 2.2.3 on 2019-08-05 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0020_remove_profile_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Backgroundphoto',
            new_name='backgroundphoto',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Headline',
            new_name='headline',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Location',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Profilephoto',
            new_name='profilephoto',
        ),
    ]
