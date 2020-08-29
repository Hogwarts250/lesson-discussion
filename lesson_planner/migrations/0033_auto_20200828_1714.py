# Generated by Django 3.1 on 2020-08-29 00:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_planner', '0032_auto_20200822_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('length', models.DurationField(null=True)),
                ('repeat', models.CharField(choices=[('never', 'Never'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='never', max_length=7)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='length',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='repeat',
        ),
        migrations.AddField(
            model_name='lesson',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lesson_planner.session'),
        ),
    ]