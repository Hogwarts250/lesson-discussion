# Generated by Django 3.1 on 2020-08-15 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0015_auto_20200811_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionrecord',
            name='users',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.DeleteModel(
            name='TransactionRecord',
        ),
    ]