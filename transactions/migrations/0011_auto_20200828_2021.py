# Generated by Django 3.1 on 2020-08-29 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0036_auto_20200828_1949'),
        ('transactions', '0010_transaction_sent_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='lesson',
        ),
        migrations.AddField(
            model_name='transaction',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lesson_planner.series'),
        ),
    ]
