# Generated by Django 2.2.3 on 2019-08-15 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0042_social_setting_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social_setting',
            name='facebook',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AlterField(
            model_name='social_setting',
            name='twitter',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AlterField(
            model_name='social_setting',
            name='website',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
    ]
