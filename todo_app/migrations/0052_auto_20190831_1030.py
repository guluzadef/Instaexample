# Generated by Django 2.2.3 on 2019-08-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0051_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='descphone',
            field=models.CharField(default=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactus',
            name='iconphone',
            field=models.CharField(default=True, max_length=255),
            preserve_default=False,
        ),
    ]