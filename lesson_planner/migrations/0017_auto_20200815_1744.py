# Generated by Django 3.1 on 2020-08-16 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0016_auto_20200815_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='date',
        ),
        migrations.AddField(
            model_name='lesson',
            name='datetime_lesson',
            field=models.DateTimeField(null=True),
        ),
    ]
