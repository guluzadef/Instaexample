# Generated by Django 2.2.3 on 2019-07-31 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_footer_footerfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='footerfields',
            name='title',
            field=models.CharField(default=True, max_length=255),
            preserve_default=False,
        ),
    ]
