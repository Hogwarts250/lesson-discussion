# Generated by Django 3.1 on 2020-08-23 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0031_lesson_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('request', 'Request'), ('create', 'Create'), ('denied', 'Denied')], default='create', max_length=7),
        ),
    ]