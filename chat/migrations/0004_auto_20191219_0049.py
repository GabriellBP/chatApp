# Generated by Django 3.0 on 2019-12-19 03:49

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_userprofile_is_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_customer',
            field=models.BooleanField(default=chat.models.set_customer),
        ),
    ]
