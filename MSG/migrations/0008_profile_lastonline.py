# Generated by Django 2.1.2 on 2018-11-03 22:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MSG', '0007_profile_isonline'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lastOnline',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 3, 22, 43, 52, 179371, tzinfo=utc)),
        ),
    ]