# Generated by Django 2.2.3 on 2019-07-31 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0014_aboutsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='mainicon')),
            ],
        ),
    ]
