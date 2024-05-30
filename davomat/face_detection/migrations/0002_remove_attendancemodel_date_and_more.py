# Generated by Django 4.2.11 on 2024-04-26 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('face_detection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancemodel',
            name='date',
        ),
        migrations.RemoveField(
            model_name='attendancemodel',
            name='time',
        ),
        migrations.AddField(
            model_name='attendancemodel',
            name='date_came',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancemodel',
            name='date_out',
            field=models.DateTimeField(auto_now=True),
        ),
    ]