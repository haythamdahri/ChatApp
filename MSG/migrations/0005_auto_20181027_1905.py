# Generated by Django 2.1.2 on 2018-10-27 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MSG', '0004_auto_20181027_1859'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roompp',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='roompp',
            name='profile1',
        ),
        migrations.RemoveField(
            model_name='roompp',
            name='profile2',
        ),
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='MSG.Profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='MSG.Profile'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RoomPP',
        ),
    ]
