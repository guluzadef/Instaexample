# Generated by Django 2.2.3 on 2019-07-31 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0011_footername'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footericon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='footername',
            name='icon',
        ),
    ]
