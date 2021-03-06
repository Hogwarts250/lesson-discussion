# Generated by Django 3.1 on 2020-08-23 00:40

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20200818_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='confirmed_denied_datetime',
        ),
        migrations.AddField(
            model_name='transaction',
            name='sent_denied_datetime',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', null=True, when={'denied', 'sent'}),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='note',
            field=models.TextField(blank=True, default=None),
        ),
    ]
