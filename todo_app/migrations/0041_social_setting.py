# Generated by Django 2.2.3 on 2019-08-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0040_auto_20190814_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social_setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.CharField(max_length=123)),
                ('facebook', models.CharField(max_length=123)),
                ('twitter', models.CharField(max_length=123)),
            ],
        ),
    ]
