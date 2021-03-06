# Generated by Django 3.1 on 2020-08-17 03:57

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0026_auto_20200816_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='transactions',
        ),
        migrations.AddField(
            model_name='lesson',
            name='confirmed_denied_datetime',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', null=True, when={'denied', 'confirmed'}),
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='pending', max_length=10, no_check_for_status=True),
        ),
    ]
